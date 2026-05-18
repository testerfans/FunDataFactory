# -*- coding: utf-8 -*- 
# @Time : 2022/6/25 23:15 
# @Author : junjie
# @File : git.py


from app.commons.settings.config import FilePath
from app.commons.utils.cmd_utils import CmdUtils
from app.commons.exceptions.global_exception import BusinessException
from urllib.parse import quote
from loguru import logger
from typing import Optional
from pathlib import Path
import os
import stat
import subprocess

class Git(object):

    @staticmethod
    def git_url(url: str, user: str, pwd: str) -> str:
        git_url_list = url.split('/')
        git_url_list[2] = f"{quote(user)}:{quote(pwd)}@" + git_url_list[2]
        return '/'.join(git_url_list)

    @staticmethod
    def git_clone_http(git_branch: str, git_url: str, user: str, password: str) -> None:
        """
        http克隆
        :param git_branch: 分支名
        :param git_url: 代码地址
        :param user: git账号
        :param password: git密码
        :return:
        """
        logger.info("http克隆开始")
        command_str = f"cd {FilePath.BASE_DIR} && " \
                      f"git clone -b {git_branch} {Git.git_url(git_url, user, password)}"
        CmdUtils.cmd(command_str)
        logger.info("http克隆结束")

    @staticmethod
    def git_clone_ssh(git_branch: str, git_url: str) -> None:
        """
        ssh克隆
        :param git_branch: 分支名
        :param git_url: 代码地址
        :return:
        """
        logger.info("ssh克隆开始")
        # 动态预置 known_hosts，避免首次连接交互确认主机指纹。
        def _extract_host(url: str) -> tuple[Optional[str], Optional[int]]:
            try:
                # 兼容 git@host:org/repo.git
                if url.startswith('git@'):
                    return url.split('@', 1)[1].split(':', 1)[0], None
                # 兼容 ssh://user@host/xxx.git
                if url.startswith('ssh://'):
                    from urllib.parse import urlparse
                    parsed = urlparse(url)
                    return parsed.hostname, parsed.port
            except Exception:
                return None, None
            return None, None

        def _known_hosts_file() -> Path:
            ssh_dir = Path.home() / ".ssh"
            ssh_dir.mkdir(mode=0o700, exist_ok=True)
            if os.name != "nt":
                ssh_dir.chmod(0o700)
            known_hosts = ssh_dir / "known_hosts"
            known_hosts.touch(exist_ok=True)
            if os.name != "nt":
                known_hosts.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
            return known_hosts

        host, port = _extract_host(git_url)
        known_hosts = _known_hosts_file()
        if host:
            keyscan_cmd = ["ssh-keyscan", "-T", "5", "-t", "rsa,ecdsa,ed25519"]
            if port:
                keyscan_cmd.extend(["-p", str(port)])
            keyscan_cmd.append(host)
            try:
                with known_hosts.open("a", encoding="utf-8") as fp:
                    subprocess.run(
                        keyscan_cmd,
                        check=True,
                        timeout=30,
                        stdout=fp,
                        stderr=subprocess.PIPE,
                        text=True,
                    )
            except (FileNotFoundError, subprocess.SubprocessError) as exc:
                logger.warning(f"写入 known_hosts 失败，将由 ssh 自动接受新主机指纹: {exc}")

        env = os.environ.copy()
        env["GIT_SSH_COMMAND"] = (
            f'ssh -i "{FilePath.RSA_PRI_KEY}" '
            f'-o StrictHostKeyChecking=accept-new '
            f'-o UserKnownHostsFile="{known_hosts}"'
        )
        try:
            subprocess.run(
                ["git", "clone", "-b", git_branch, git_url],
                cwd=FilePath.BASE_DIR,
                env=env,
                check=True,
                timeout=180,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        except Exception as exc:
            logger.error(f"ssh克隆失败, 错误信息: {str(exc)}")
            raise BusinessException("命令执行失败!!! ")
        logger.info("ssh克隆结束")

    @staticmethod
    def git_pull(project_path: str, git_branch: str) -> None:
        """
        拉取代码
        :param project_path: 项目路径
        :param git_branch: 代码分支
        :return:
        """
        logger.info("拉取项目代码开始")
        command_str = f"cd {project_path} && " \
                      f"git fetch --all && " \
                      f"git reset --hard origin/{git_branch}"
        CmdUtils.cmd(command_str)
        logger.info("拉取项目代码结束")

    @staticmethod
    def project_install(project_path: str):
        logger.info("更新依赖开始")
        command_str = f"cd {project_path} && " \
                      f"pip install -r requirements.txt --default-timeout=60 -i https://pypi.tuna.tsinghua.edu.cn/simple"
        p = CmdUtils.cmd(command_str, timeout=60)
        logger.info("更新依赖结束")
        return p.stdout

if __name__ == '__main__':
    url = 'git@gitee.com:JokerChat/img.git'
    branch = 'master'
    Git.git_clone_ssh(branch, url)
