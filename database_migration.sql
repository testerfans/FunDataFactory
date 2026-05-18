-- 数据库迁移脚本

-- 1. 为 data_factory_run_log 表添加缺失字段
ALTER TABLE data_factory_run_log 
ADD COLUMN requests_id VARCHAR(64) NOT NULL DEFAULT '' COMMENT '请求id';

ALTER TABLE data_factory_run_log 
ADD COLUMN project_id INT NOT NULL DEFAULT 0 COMMENT '项目id';

ALTER TABLE data_factory_run_log 
CHANGE COLUMN run_params run_param_in TEXT NULL COMMENT '实际入参';

ALTER TABLE data_factory_run_log 
CHANGE COLUMN run_result run_param_out TEXT NULL COMMENT '实际出参';

-- 2. 为 data_factory_cases 表添加手动执行时间字段
ALTER TABLE data_factory_cases 
ADD COLUMN manual_execution_time INT DEFAULT 0 COMMENT '手动执行时间（秒）';

-- 3. 为 data_factory_run_log 表添加执行时长字段
ALTER TABLE data_factory_run_log 
ADD COLUMN cost VARCHAR(20) NULL COMMENT '执行时长（秒）';

-- 4. 为现有数据设置默认的手动执行时间（可以根据实际情况调整）
-- 这里设置为30秒作为示例，实际使用时应该根据每个场景的具体情况设置
UPDATE data_factory_cases 
SET manual_execution_time = 30 
WHERE manual_execution_time = 0;

-- 5. 创建索引以提高查询性能（可选）
CREATE INDEX idx_run_log_cases_id ON data_factory_run_log(cases_id);
CREATE INDEX idx_run_log_run_status ON data_factory_run_log(run_status);
CREATE INDEX idx_cases_manual_time ON data_factory_cases(manual_execution_time);
