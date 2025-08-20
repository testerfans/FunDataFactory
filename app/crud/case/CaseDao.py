# -*- coding: utf-8 -*-
# @Time : 2022/8/21 20:27
# @Author : junjie
# @File : CasesDao.py

from app.models.cases import DataFactoryCases
from app.models.project import DataFactoryProject
from app.models.cases_like import DataFactoryCasesLike
from app.models.cases_collection import DataFactoryCasesCollection
from app.models.cases_params import DataFactoryCasesParams
from app.routers.cases.response_model.cases_out import CaseDto, CaseGroupDto, CaseSearchDto, CasesParamsDto
from app.routers.cases.request_model.cases_in import AddCasesParams, EditCasesParmas
from app.commons.exceptions.global_exception import BusinessException
from app.crud.project.ProjectDao import ProjectDao
from app.crud.project_role.ProjectRoleDao import ProjectRoleDao
from loguru import logger
from app.crud import BaseCrud
from sqlalchemy import or_, asc, and_, func, case as case_, distinct, INT
from sqlalchemy.orm import aliased
from app.models import Session
from app.const.enums import DeleteEnum, ShowEnum
from datetime import datetime
from app.models.run_log import DataFactoryRunLog
import re

class CaseDao(BaseCrud):

    log = logger
    model = DataFactoryCases

    @classmethod
    def insert_case(cls, project_id: int , title: str, name: str, description: str, group_name: str, header: str, owner: str, path: str,
                    param_in: str, param_out: str, example_param_in: str, example_param_out: str, manual_execution_time: int = 0, user: dict = None) -> None:
        """
        新增造数场景
        :param project_id: 项目id
        :param title: 标题
        :param name: 方法名
        :param description: 描述信息
        :param group_name: 分组名
        :param header: 请求头
        :param owner: 负责人
        :param path: 路径
        :param param_in: 请求参数
        :param param_out: 返回参数
        :param example_param_in: 请求示例
        :param example_param_out: 返回示例
        :param manual_execution_time: 手动执行时间（秒）
        :param user: 用户数据
        :return:
        """
        ant = cls.get_with_existed(project_id = project_id, name = name)
        if ant:
            raise BusinessException("造数场景已存在！！！")
        case = DataFactoryCases(project_id, title, name, description, group_name, header, owner, path, param_in,
                                 param_out, example_param_in, example_param_out, manual_execution_time, user)
        cls.insert_by_model(model_obj = case)

    @classmethod
    def update_case(cls, cases_id: int, title: str, name: str, description: str, group_name: str, header: str, owner: str, path: str,
                    param_in: str, param_out: str, example_param_in: str, example_param_out: str, manual_execution_time: int = 0, user: dict = None) -> None:
        """
        更新造数场景
        :param cases_id: 主键id
        :param title: 标题
        :param name: 方法名
        :param description: 描述信息
        :param group_name: 分组名
        :param header: 请求头
        :param owner: 负责人
        :param path: 路径
        :param param_in: 请求参数
        :param param_out: 返回参数
        :param example_param_in: 请求示例
        :param example_param_out: 返回示例
        :param manual_execution_time: 手动执行时间（秒）
        :param user: 用户数据
        :return:
        """
        ant = cls.get_with_existed(id=cases_id)
        if not ant:
            raise BusinessException("造数场景不存在！！！")
        update_map = {
            "id": cases_id,
            "title": title,
            "name": name,
            "description": description,
            "group_name": group_name,
            "header": header,
            "owner": owner,
            "path": path,
            "param_in": param_in,
            "param_out": param_out,
            "example_param_in": example_param_in,
            "example_param_out": example_param_out,
            "manual_execution_time": manual_execution_time
        }
        cls.update_by_id(model = update_map, user = user)


    @classmethod
    def delete_case(cls, cases_id: int, user: dict) -> None:
        """
        删除造数场景
        :param cases_id: 主键id
        :param user: 用户数据
        :return:
        """
        ant = cls.get_with_existed(id=cases_id)
        if not ant:
            raise BusinessException("造数场景不存在！！！")
        cls.delete_by_id(id = cases_id, user = user)

    @classmethod
    def get_projet_case(cls, project_id: int) -> DataFactoryCases:
        """
        获取项目下的所有造数场景
        :param project_id: 项目id
        :return:
        """
        case_infos = cls.get_with_params(project_id = project_id, _fields = CaseDto)
        return case_infos

    @classmethod
    def project_ids(cls, user: dict):
        """
        获取用户所拥有的项目id
        :param user: 用户数据
        :return:
        """
        filter_list = []
        project_ids = [i[0] for i in ProjectDao.get_user_all_projects(user)]
        filter_list.append(DataFactoryCases.project_id.in_(project_ids))
        return filter_list

    @classmethod
    def get_user_group_name(cls, user: dict):
        """
        获取用户权限范围内的业务线
        :param user:
        :return:
        """
        groups = cls.get_with_params(filter_list = [ *cls.project_ids(user) ],
                                     _fields = CaseGroupDto, _group = [DataFactoryCases.group_name])
        return groups

    @classmethod
    def get_search_case(cls, user: dict, keyword: str):
        """
        模糊搜索用例，用于前端查询
        :param user: 用户数据
        :param keyword: 搜索内容
        :return:
        """
        filter_list = []
        search_str = f"%{keyword}%"
        filter_list.append(or_(DataFactoryCases.name.like(search_str),
                               DataFactoryCases.title.like(search_str),
                               DataFactoryCases.owner.like(search_str),
                               DataFactoryCases.description.like(search_str),
                               ))
        filter_list.extend(cls.project_ids(user))
        cases = cls.get_with_params(filter_list = filter_list, _fields = CaseSearchDto)
        return cases

    @classmethod
    def get_all_cases(cls, user: dict, page: int = 1, limit: int = 10, show: str = None, project_id: int = None, case_id: int = None):
        """
        用例列表展示
        :param user: 用户数据
        :param page: 页码
        :param limit: 页码大小
        :param show: 筛选类型
        :param project_id: 项目id
        :param case_id: 用例id
        :return:
        """
        with Session() as session:
            # 别名
            like_ = aliased(DataFactoryCasesLike)
            collection_ = aliased(DataFactoryCasesCollection)

            # 只取未删除的数据
            filter_list = [DataFactoryCases.del_flag == DeleteEnum.no.value]
            # 如果like_表中 del_flag字段标识为0则为已点赞=True，其余情况为未点赞=False
            is_like = case_([(like_.del_flag == DeleteEnum.no.value, True)], else_=False).label("like")
            # 如果collection_表中 del_flag字段标识为0则为已收藏=True，其余情况为未收藏=False
            is_collection = case_([(collection_.del_flag == DeleteEnum.no.value, True)], else_=False).label("collection")

            # 子表-统计各造数场景点赞数和收藏数, 子查询(subquery)
            summary = session.query(DataFactoryCases.id.label("cases_id"),
                                    func.count(distinct(like_.id)).label("like_num"),
                                    func.count(distinct(collection_.id)).label("collection_num")). \
                outerjoin(like_, and_(DataFactoryCases.id == like_.cases_id,
                                     like_.del_flag == 0)). \
                outerjoin(collection_, and_(DataFactoryCases.id == collection_.cases_id,
                                           collection_.del_flag == 0)).group_by(DataFactoryCases.id).subquery()

            # 为null的数据默认为0
            like_num = func.ifnull(summary.c.like_num, 0).label("like_num")
            collection_num = func.ifnull(summary.c.collection_num, 0).label("collection_num")

            # 用户有效的项目id
            filter_list.extend(cls.project_ids(user))
            # 根据项目id查询
            if project_id:
                filter_list.append(DataFactoryCases.project_id == project_id)
            # 根据case id查询
            if case_id:
                filter_list.append(DataFactoryCases.id == case_id)

            if show:
                if show in ShowEnum.get_member_values():
                    # 获取我创建的
                    if show == ShowEnum.my.value:
                        filter_list.append(DataFactoryCases.owner == user['username'])
                    # 获取我的喜欢
                    elif show == ShowEnum.like.value:
                        my_like = [like_.create_id == user['id'], like_.del_flag == 0]
                        filter_list.extend(my_like)
                    # 获取我的收藏
                    elif show == ShowEnum.collection.value:
                        my_collection = [collection_.create_id == user['id'], collection_.del_flag == 0]
                        filter_list.extend(my_collection)
                    elif show == ShowEnum.all.value:
                        pass
                    else:
                        raise BusinessException("类型有误！！！")
                else:
                    # 业务线分组
                    filter_list.append(DataFactoryCases.group_name == show)

            # cases主表关联like表、collection表、summary表
            case = session.query(like_num, collection_num, DataFactoryCases.project_id, DataFactoryCases.id,
                                 DataFactoryCases.title, DataFactoryCases.group_name, DataFactoryCases.description,
                                 DataFactoryCases.owner, is_like, is_collection, DataFactoryCases.update_time,
                                 DataFactoryCases.manual_execution_time). \
                outerjoin(like_, and_(DataFactoryCases.id == like_.cases_id,
                                     like_.del_flag == 0,
                                     like_.create_id == user['id'])). \
                outerjoin(collection_, and_(DataFactoryCases.id == collection_.cases_id,
                                           collection_.del_flag == 0,
                                           collection_.create_id == user['id'])). \
                outerjoin(summary, DataFactoryCases.id == summary.c.cases_id)

            # 过滤条件
            case = case.filter(*filter_list)
            # 分页
            case_infos = case.order_by(asc(DataFactoryCases.id)).limit(limit).offset((page - 1) * limit).all()
            count = case.count()
            return case_infos, count


    @classmethod
    def case_detail_by_id(cls, id: int, user: dict = None):
        """
        获取某个造数场景
        :param id: 用例id
        :param user: 用户数据
        :return:
        """
        with Session() as session:
            case = session.query(DataFactoryCases.owner, DataFactoryCases.group_name, DataFactoryCases.description, DataFactoryCases.create_name, DataFactoryCases.create_time, DataFactoryCases.update_time,
                                 DataFactoryCases.id, DataFactoryCases.path, DataFactoryCases.project_id, DataFactoryCases.name, DataFactoryCases.example_param_in, DataFactoryCases.example_param_out,
                                 DataFactoryCases.param_in, DataFactoryCases.param_out, DataFactoryCases.title, DataFactoryCases.manual_execution_time, DataFactoryProject.project_name, DataFactoryProject.git_project, DataFactoryProject.directory).\
                join(DataFactoryCases, DataFactoryCases.project_id == DataFactoryProject.id).\
                filter(DataFactoryCases.id == id,DataFactoryCases.del_flag == 0).first()
            if user:
                ProjectRoleDao.read_permission(case.project_id, user)
            if case is None:
                raise BusinessException("场景不存在")
            return case

    @classmethod
    def delete_project_case(cls, session: Session, project_id: int, user: dict) -> list:
        """
        删除所有造数场景
        :param session: 数据库会话
        :param project_id: 项目id
        :param user: 用户数据
        :return:
        """
        filter_list = [DataFactoryCases.project_id == project_id, DataFactoryCases.del_flag == DeleteEnum.no.value ]
        cases = cls.update_by_map(session = session, filter_list = filter_list, user = user, del_flag = DeleteEnum.yes.value)
        return [i.id for i in cases]

    @classmethod
    def case_detail_by_method(cls, name: str):
        """
        根据方法查询case信息
        :param name: 方法名
        :return:
        """
        with Session() as session:
            case = session.query(DataFactoryCases.id.label("cases_id"), DataFactoryCases.path, DataFactoryCases.project_id, DataFactoryCases.name.label("method"), DataFactoryProject.git_project.label("project"), DataFactoryProject.directory). \
                join(DataFactoryCases, DataFactoryCases.project_id == DataFactoryProject.id). \
                filter(DataFactoryCases.name == name, DataFactoryCases.del_flag == 0).first()
            if case is None:
                raise Exception("场景不存在")
            return case

    @classmethod
    def case_summary(cls):
        """统计场景数量"""
        case_sum = cls.get_with_count()
        return case_sum

    @classmethod
    def get_efficiency_stats(cls, cases_id: int = None, group_name: str = None, project_id: int = None):
        """
        获取提效统计信息
        :param cases_id: 场景ID（可选）
        :param group_name: 业务线名称（可选）
        :param project_id: 项目ID（可选）
        :return: 提效统计信息
        """
        with Session() as session:
            # 构建查询条件
            filter_list = [DataFactoryCases.del_flag == DeleteEnum.no.value]
            
            if cases_id:
                filter_list.append(DataFactoryCases.id == cases_id)
            if group_name:
                filter_list.append(DataFactoryCases.group_name == group_name)
            if project_id:
                filter_list.append(DataFactoryCases.project_id == project_id)
            
            # 查询场景信息
            cases_query = session.query(
                DataFactoryCases.id,
                DataFactoryCases.title,
                DataFactoryCases.group_name,
                DataFactoryCases.manual_execution_time,
                func.count(DataFactoryRunLog.id).label('total_executions'),
                func.sum(case_(
                    (DataFactoryRunLog.run_status == 0, 1),  # 成功执行
                    else_=0
                )).label('success_executions'),
                func.sum(case_(
                    (DataFactoryRunLog.run_status == 0, DataFactoryRunLog.cost),  # 成功执行的时间
                    else_=None
                )).label('total_auto_time')
            ).outerjoin(
                DataFactoryRunLog, 
                DataFactoryCases.id == DataFactoryRunLog.cases_id
            ).filter(*filter_list).group_by(
                DataFactoryCases.id,
                DataFactoryCases.title,
                DataFactoryCases.group_name,
                DataFactoryCases.manual_execution_time
            )
            
            cases_stats = cases_query.all()
            
            # 计算提效统计（按成功执行次数累计手动时间）
            total_efficiency_time = 0
            total_manual_time = 0
            total_auto_time = 0
            total_success_count = 0
            
            for case_stat in cases_stats:
                manual_time = case_stat.manual_execution_time or 0
                success_count = case_stat.success_executions or 0
                
                # 处理自动执行时间（字符串格式如 "1.23s"）
                auto_time_str = case_stat.total_auto_time
                auto_time = 0
                if auto_time_str:
                    # 提取数字部分，去掉"s"后缀
                    match = re.search(r'(\d+\.?\d*)s?', str(auto_time_str))
                    if match:
                        auto_time = float(match.group(1))
                
                # 计算提效时间：成功次数 × 手动时间 - 累计自动时间
                # 确保数据类型一致，将Decimal转换为float
                manual_time_float = float(manual_time) if manual_time else 0.0
                success_count_float = float(success_count) if success_count else 0.0
                efficiency_time = success_count_float * manual_time_float - auto_time
                
                # 累计总手动时间：成功次数 × 单次手动时间
                total_manual_time += (success_count_float * manual_time_float)
                total_auto_time += auto_time
                total_success_count += float(success_count) if success_count else 0.0
                total_efficiency_time += efficiency_time
            
            return {
                'cases_stats': cases_stats,
                'summary': {
                    'total_efficiency_time': total_efficiency_time,
                    'total_manual_time': total_manual_time,
                    'total_auto_time': total_auto_time,
                    'total_success_count': total_success_count
                }
            }

    @classmethod
    def get_team_efficiency_stats(cls):
        """
        获取团队整体提效统计
        :return: 团队提效统计信息
        """
        with Session() as session:
            # 按业务线分组统计
            group_stats = session.query(
                DataFactoryCases.group_name,
                # 仅统计成功执行的手动时间：成功次数 × 手动时间
                func.sum(case_(
                    (DataFactoryRunLog.run_status == 0, DataFactoryCases.manual_execution_time),
                    else_=0
                )).label('total_manual_time'),
                func.count(DataFactoryRunLog.id).label('total_executions'),
                func.sum(case_(
                    (DataFactoryRunLog.run_status == 0, 1),
                    else_=0
                )).label('success_executions'),
                func.sum(case_(
                    (DataFactoryRunLog.run_status == 0, DataFactoryRunLog.cost),
                    else_=None
                )).label('total_auto_time')
            ).outerjoin(
                DataFactoryRunLog,
                DataFactoryCases.id == DataFactoryRunLog.cases_id
            ).filter(
                DataFactoryCases.del_flag == DeleteEnum.no.value
            ).group_by(
                DataFactoryCases.group_name
            ).all()
            
            # 计算总体统计
            total_efficiency_time = 0
            total_manual_time = 0
            total_auto_time = 0
            total_success_count = 0
            
            for group_stat in group_stats:
                manual_time = group_stat.total_manual_time or 0
                success_count = group_stat.success_executions or 0
                
                # 处理自动执行时间（字符串格式如 "1.23s"）
                auto_time_str = group_stat.total_auto_time
                auto_time = 0
                if auto_time_str:
                    # 提取数字部分，去掉"s"后缀
                    match = re.search(r'(\d+\.?\d*)s?', str(auto_time_str))
                    if match:
                        auto_time = float(match.group(1))
                
                # 确保数据类型一致，将Decimal转换为float
                manual_time_float = float(manual_time) if manual_time else 0.0
                success_count_float = float(success_count) if success_count else 0.0
                efficiency_time = success_count_float * manual_time_float - auto_time
                
                # 确保数据类型一致，将Decimal转换为float
                total_manual_time += float(manual_time) if manual_time else 0.0
                total_auto_time += auto_time
                total_success_count += float(success_count) if success_count else 0.0
                total_efficiency_time += efficiency_time
            
            return {
                'group_stats': group_stats,
                'team_summary': {
                    'total_efficiency_time': total_efficiency_time,
                    'total_manual_time': total_manual_time,
                    'total_auto_time': total_auto_time,
                    'total_success_count': total_success_count
                }
            }

    @classmethod
    def case_group_summary(cls):
        """统计各业务线数量"""
        with Session() as session:
            group_num = session.query(DataFactoryCases.group_name.label("name"), func.count(DataFactoryCases.id).label("value"))\
                .filter(DataFactoryCases.del_flag == 0)\
                .group_by(DataFactoryCases.group_name)
            return group_num.all()

    @classmethod
    def get_group_name(cls):
        """所有业务数"""
        with Session() as session:
            filter_list = [DataFactoryCases.del_flag == 0]
            query = session.query(DataFactoryCases.group_name).filter(*filter_list)
            groups = query.group_by(DataFactoryCases.group_name).all()
            return groups

    @classmethod
    def collect_weekly_data(cls, start_time: datetime, end_time: datetime):
        """统计最近7天场景创建量"""
        with Session() as session:
            date = func.date_format(DataFactoryCases.create_time, "%Y-%m-%d")
            weekly_data = session.query(date.label("date"), func.count(DataFactoryCases.id).label("sum"))\
                .filter(DataFactoryCases.del_flag ==0, DataFactoryCases.create_time.between(start_time.strftime("%Y-%m-%d 00:00:00"), end_time.strftime("%Y-%m-%d 23:59:59"))).\
                group_by(date).order_by(asc(date))
            data = {i[0]:i[1] for i in weekly_data.all()}
            return data

class CaseParamsDao(BaseCrud):
    log = logger
    model = DataFactoryCasesParams

    @classmethod
    def insert_cases_params(cls, body: AddCasesParams, out_id: str, user: dict):
        """
        新增场景参数组合
        :param body: 参数组合模型
        :param out_id: 外链id
        :param user: 用户数据
        :return:
        """
        with Session() as session:
            case = session.query(DataFactoryCases).filter(DataFactoryCases.id == body.cases_id,
                                                          DataFactoryCases.del_flag == 0).first()
            if not case:
                raise BusinessException("造数场景不存在！！！")
            filter_list = [
                DataFactoryCasesParams.cases_id == body.cases_id,
                or_(DataFactoryCasesParams.out_id == out_id,
                    DataFactoryCasesParams.name == body.name,
                    DataFactoryCasesParams.params == body.params,
                    )
            ]
            result = cls.get_with_existed(session = session, filter_list = filter_list)
            if result:
                raise BusinessException("该参数组合已存在，请重新录入！")
            cases_params = DataFactoryCasesParams(**body.dict(), out_id = out_id, user = user)
            cls.insert_by_model(session = session, model_obj = cases_params)


    @classmethod
    def update_cases_params(cls, body: EditCasesParmas, user: dict):
        """
        编辑场景参数组合
        :param body: 编辑参数组合模型
        :param user: 用户数据
        :return:
        """
        with Session() as session:
            case = session.query(DataFactoryCases).filter(DataFactoryCases.id == body.cases_id,
                                                          DataFactoryCases.del_flag == 0).first()
            if not case:
                raise BusinessException("造数场景不存在！！！")
            param_result = cls.get_with_existed(session = session, id = body.id)
            if not param_result: raise BusinessException("参数组合数据不存在！")
            # 根据名称查出数据
            params_name = cls.get_with_first(session = session, name = body.name, cases_id = body.cases_id)
            # 如果有数据且主键id与请求参数id不相等
            if params_name is not None and params_name.id != body.id:
                raise BusinessException("参数组合名称重复, 请重新录入！！！")
            cls.update_by_id(session = session, model = body, user = user)

    @classmethod
    def deleta_cases_params(cls, id: int, user: dict):
        """
        删除场景参数组合
        :param id: 主键id
        :param user: 用户数据
        :return:
        """
        with Session() as session:
            param_result = session.query(DataFactoryCasesParams).filter(DataFactoryCasesParams.id == id,
                                                                        DataFactoryCasesParams.del_flag == 0).first()
            if param_result is None: raise BusinessException("参数组合数据不存在！")

            cls.delete_by_id(session = session, id = id, user = user)

    @classmethod
    def get_cases_params(cls, cases_id: int, page=1, limit=10):
        """
        获取某个造数场景的参数组合
        :param cases_id: 用例id
        :param page: 页码
        :param limit: 页码大小
        :return:
        """
        total, params_infos = cls.get_with_pagination(page = page, limit = limit, _fields = CasesParamsDto,
                                                      cases_id = cases_id)
        return total, params_infos

    @classmethod
    def delete_all_params(cls, session: Session, cases_id: list, user: dict):
        filter_list = [
            DataFactoryCasesParams.cases_id.in_(cases_id), DataFactoryCasesParams.del_flag == DeleteEnum.no.value
        ]
        cls.update_by_map(session = session, filter_list = filter_list, user = user, del_flag = DeleteEnum.yes.value)


    @classmethod
    def get_params_detail(cls, out_id: str):
        """根据外链id获取参数组合信息"""
        param_result = cls.get_with_first(out_id = out_id)
        if param_result is None: raise BusinessException("参数组合数据不存在！")
        return param_result