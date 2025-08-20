# -*- coding: utf-8 -*- 
# @Time : 2022/9/18 19:07 
# @Author : junjie
# @File : data_logic.py

from app.crud.project.ProjectDao import ProjectDao
from app.crud.case.CaseDao import CaseDao
from app.crud.log.LogDao import LogDao
from app.crud.user.UserDao import UserDao
from datetime import datetime, timedelta




def data_summary_logic():
    # 用户数
    user_num = UserDao.user_summary()
    # 项目数
    project_num = ProjectDao.project_summary()
    # 场景数
    case_num = CaseDao.case_summary()
    # 业务线数
    group_num = CaseDao.get_group_name()
    # 调用量数
    log_num = LogDao.log_summary()

    # 成功率计算
    success_num = LogDao.success_summary()
    success_rate = success_num / log_num if log_num !=0 else 0

    # 各状态分布
    run_type_data = LogDao.run_status_summary()

    # 各调用方式分布
    call_type_data = LogDao.call_type_summary()

    # 统计各业务线分布
    group_case_num = CaseDao.case_group_summary()

    # 最近7天调用量
    today = datetime.today()
    last_7_day = (today - timedelta(days=6))
    weekly_data = LogDao.collect_weekly_data(last_7_day, today)

    return dict(user=user_num, project=project_num, case=case_num,
                 group = len(group_num), log=log_num, success_rate = '{:.2f}%'.format(success_rate*100),
                run_type_data = run_type_data, call_type_data = call_type_data,
                group_data = group_case_num, weekly_data = weekly_data)


def time_saving_summary_logic():
    """
    时间节省统计逻辑
    计算场景、业务线和整个部门通过数据构造平台节省的时间
    """
    # 获取场景级别的时间节省统计
    cases_efficiency = CaseDao.get_efficiency_stats()
    
    # 获取业务线级别的时间节省统计
    team_efficiency = CaseDao.get_team_efficiency_stats()
    
    # 计算总体节省时间
    # 确保数据类型一致，将Decimal转换为float
    total_saved_time = float(cases_efficiency['summary']['total_efficiency_time']) if cases_efficiency['summary']['total_efficiency_time'] else 0.0
    total_manual_time = float(cases_efficiency['summary']['total_manual_time']) if cases_efficiency['summary']['total_manual_time'] else 0.0
    total_auto_time = float(cases_efficiency['summary']['total_auto_time']) if cases_efficiency['summary']['total_auto_time'] else 0.0
    total_success_count = cases_efficiency['summary']['total_success_count']
    
    # 格式化时间显示
    def format_time(seconds):
        if seconds < 60:
            return f"{seconds:.1f}秒"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}分钟"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}小时"
    
    # 计算每个业务线的节省时间
    business_lines_data = []
    for group_stat in team_efficiency['group_stats']:
        # 这里的 total_manual_time 已是“仅成功的手动时间累计”
        manual_time = group_stat.total_manual_time or 0
        success_count = group_stat.success_executions or 0
        
        # 处理自动执行时间（字符串格式如 "1.23s"）
        auto_time_str = group_stat.total_auto_time
        auto_time = 0
        if auto_time_str:
            import re
            match = re.search(r'(\d+\.?\d*)s?', str(auto_time_str))
            if match:
                auto_time = float(match.group(1))
        
        # 计算节省时间：累计手动时间 - 累计自动时间（两者均为成功执行产生）
        manual_time_float = float(manual_time) if manual_time else 0.0
        efficiency_time = manual_time_float - auto_time
        
        business_lines_data.append({
            'group_name': group_stat.group_name,
            'saved_time': format_time(efficiency_time),
            'manual_time': format_time(manual_time),
            'auto_time': format_time(auto_time),
            'success_count': success_count,
            'total_executions': group_stat.total_executions or 0
        })
    
    # 计算每个场景的节省时间
    top_cases_data = []
    for case_stat in cases_efficiency['cases_stats']:
        manual_time = case_stat.manual_execution_time or 0
        success_count = case_stat.success_executions or 0
        
        # 处理自动执行时间（字符串格式如 "1.23s"）
        auto_time_str = case_stat.total_auto_time
        auto_time = 0
        if auto_time_str:
            import re
            match = re.search(r'(\d+\.?\d*)s?', str(auto_time_str))
            if match:
                auto_time = float(match.group(1))
        
        # 计算节省时间（场景级）：成功次数 × 单次手动时间 - 累计自动时间
        manual_time_float = float(manual_time) if manual_time else 0.0
        success_count_float = float(success_count) if success_count else 0.0
        efficiency_time = success_count_float * manual_time_float - auto_time
        
        top_cases_data.append({
            'title': case_stat.title,
            'group_name': case_stat.group_name,
            'saved_time': format_time(efficiency_time),
            'manual_time': format_time(manual_time),
            'success_count': success_count,
            'total_executions': case_stat.total_executions or 0
        })
    
    # 按节省时间排序，取前10名
    def parse_time_to_seconds(time_str):
        if '秒' in time_str:
            return float(time_str.replace('秒', ''))
        elif '分钟' in time_str:
            return float(time_str.replace('分钟', '')) * 60
        elif '小时' in time_str:
            return float(time_str.replace('小时', '')) * 3600
        else:
            return 0
    
    top_cases_data.sort(key=lambda x: parse_time_to_seconds(x['saved_time']), reverse=True)
    
    return {
        'department_summary': {
            'total_saved_time': format_time(total_saved_time),
            'total_manual_time': format_time(total_manual_time),
            'total_auto_time': format_time(total_auto_time),
            'total_success_count': total_success_count,
            'efficiency_rate': f"{(total_saved_time / total_manual_time * 100):.1f}%" if total_manual_time > 0 else "0%"
        },
        'business_lines': business_lines_data,
        'top_cases': top_cases_data[:10]  # 取前10名
    }