-- 数据库迁移脚本：为提效统计功能添加必要字段

-- 1. 为 data_factory_cases 表添加手动执行时间字段
ALTER TABLE data_factory_cases 
ADD COLUMN manual_execution_time INT DEFAULT 0 COMMENT '手动执行时间（秒）';

-- 2. 为 data_factory_run_log 表添加执行时长字段
ALTER TABLE data_factory_run_log 
ADD COLUMN cost VARCHAR(20) NULL COMMENT '执行时长（秒）';

-- 3. 为现有数据设置默认的手动执行时间（可以根据实际情况调整）
-- 这里设置为30秒作为示例，实际使用时应该根据每个场景的具体情况设置
UPDATE data_factory_cases 
SET manual_execution_time = 30 
WHERE manual_execution_time = 0;

-- 4. 创建索引以提高查询性能（可选）
CREATE INDEX idx_run_log_cases_id ON data_factory_run_log(cases_id);
CREATE INDEX idx_run_log_run_status ON data_factory_run_log(run_status);
CREATE INDEX idx_cases_manual_time ON data_factory_cases(manual_execution_time);
