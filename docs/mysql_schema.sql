-- AI八字算命助手 MySQL 8+ 生产版建表脚本

-- =========================
-- 1. 用户表
-- =========================
CREATE TABLE app_user (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_no VARCHAR(32) NOT NULL UNIQUE,
    login_type VARCHAR(20) NOT NULL,
    mobile VARCHAR(32),
    mobile_masked VARCHAR(32),
    wechat_openid VARCHAR(128),
    nickname VARCHAR(64),
    gender VARCHAR(16),
    timezone VARCHAR(64) NOT NULL DEFAULT 'Asia/Shanghai',
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    register_source VARCHAR(32),
    last_active_at DATETIME,
    is_deleted TINYINT(1) NOT NULL DEFAULT 0,
    deleted_at DATETIME,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT chk_app_user_login_type CHECK (login_type IN ('guest', 'mobile', 'wechat')),
    CONSTRAINT chk_app_user_status CHECK (status IN ('active', 'disabled', 'deleted')),
    CONSTRAINT chk_app_user_gender CHECK (gender IS NULL OR gender IN ('male', 'female', 'other'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_app_user_mobile ON app_user(mobile);
CREATE INDEX idx_app_user_openid ON app_user(wechat_openid);
CREATE INDEX idx_app_user_status ON app_user(status);

-- =========================
-- 2. 八字档案表
-- =========================
CREATE TABLE bazi_profile (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    profile_no VARCHAR(32) NOT NULL UNIQUE,
    name VARCHAR(64),
    gender VARCHAR(16) NOT NULL,
    calendar_type VARCHAR(16) NOT NULL DEFAULT 'solar',
    birth_date DATE NOT NULL,
    birth_time TIME,
    birth_time_unknown TINYINT(1) NOT NULL DEFAULT 0,
    birth_country VARCHAR(64),
    birth_province VARCHAR(64),
    birth_city VARCHAR(64),
    birth_place_text VARCHAR(255),
    birth_place_masked VARCHAR(255),
    timezone VARCHAR(64) NOT NULL DEFAULT 'Asia/Shanghai',
    birth_date_encrypted TEXT,
    birth_time_encrypted TEXT,
    birth_place_encrypted TEXT,
    bazi_chart_json JSON,
    chart_source VARCHAR(32),
    chart_version VARCHAR(32),
    version_no INT NOT NULL DEFAULT 1,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    is_deleted TINYINT(1) NOT NULL DEFAULT 0,
    deleted_at DATETIME,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_bazi_profile_user FOREIGN KEY (user_id) REFERENCES app_user(id),
    CONSTRAINT chk_bazi_profile_gender CHECK (gender IN ('male', 'female', 'other')),
    CONSTRAINT chk_bazi_profile_calendar_type CHECK (calendar_type IN ('solar', 'lunar'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_bazi_profile_user ON bazi_profile(user_id);
CREATE INDEX idx_bazi_profile_user_active ON bazi_profile(user_id, is_active);
CREATE INDEX idx_bazi_profile_deleted ON bazi_profile(is_deleted);

-- =========================
-- 3. 命盘解读表
-- =========================
CREATE TABLE natal_reading (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    profile_id BIGINT NOT NULL,
    reading_no VARCHAR(32) NOT NULL UNIQUE,
    content_mode VARCHAR(16) NOT NULL DEFAULT 'plain',
    generation_mode VARCHAR(16) NOT NULL DEFAULT 'hybrid',
    personality_text TEXT,
    strengths_text TEXT,
    risks_text TEXT,
    advice_text TEXT,
    summary_text TEXT,
    disclaimer_text VARCHAR(500),
    content_json JSON,
    llm_model VARCHAR(64),
    prompt_version VARCHAR(32),
    review_status VARCHAR(20) NOT NULL DEFAULT 'approved',
    risk_level VARCHAR(20) NOT NULL DEFAULT 'low',
    status VARCHAR(20) NOT NULL DEFAULT 'ready',
    generated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_deleted TINYINT(1) NOT NULL DEFAULT 0,
    deleted_at DATETIME,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_natal_reading_user FOREIGN KEY (user_id) REFERENCES app_user(id),
    CONSTRAINT fk_natal_reading_profile FOREIGN KEY (profile_id) REFERENCES bazi_profile(id),
    CONSTRAINT chk_natal_reading_content_mode CHECK (content_mode IN ('plain', 'professional')),
    CONSTRAINT chk_natal_reading_generation_mode CHECK (generation_mode IN ('rule', 'llm', 'hybrid')),
    CONSTRAINT chk_natal_reading_review_status CHECK (review_status IN ('pending', 'approved', 'rejected')),
    CONSTRAINT chk_natal_reading_risk_level CHECK (risk_level IN ('low', 'medium', 'high')),
    CONSTRAINT chk_natal_reading_status CHECK (status IN ('ready', 'failed', 'archived'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_natal_reading_user_profile ON natal_reading(user_id, profile_id);
CREATE INDEX idx_natal_reading_generated_at ON natal_reading(generated_at);

-- =========================
-- 4. 每日运势表
-- =========================
CREATE TABLE daily_fortune (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    profile_id BIGINT NOT NULL,
    fortune_date DATE NOT NULL,
    score SMALLINT,
    keyword_tags VARCHAR(255),
    favorable_text TEXT,
    unfavorable_text TEXT,
    advice_text TEXT,
    summary_text TEXT,
    detail_json JSON,
    generation_mode VARCHAR(16) NOT NULL DEFAULT 'hybrid',
    llm_model VARCHAR(64),
    prompt_version VARCHAR(32),
    review_status VARCHAR(20) NOT NULL DEFAULT 'approved',
    risk_level VARCHAR(20) NOT NULL DEFAULT 'low',
    is_fixed TINYINT(1) NOT NULL DEFAULT 1,
    generated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_deleted TINYINT(1) NOT NULL DEFAULT 0,
    deleted_at DATETIME,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT uk_daily_fortune UNIQUE (user_id, profile_id, fortune_date),
    CONSTRAINT fk_daily_fortune_user FOREIGN KEY (user_id) REFERENCES app_user(id),
    CONSTRAINT fk_daily_fortune_profile FOREIGN KEY (profile_id) REFERENCES bazi_profile(id),
    CONSTRAINT chk_daily_fortune_score CHECK (score IS NULL OR score BETWEEN 0 AND 100),
    CONSTRAINT chk_daily_fortune_generation_mode CHECK (generation_mode IN ('rule', 'llm', 'hybrid')),
    CONSTRAINT chk_daily_fortune_review_status CHECK (review_status IN ('pending', 'approved', 'rejected')),
    CONSTRAINT chk_daily_fortune_risk_level CHECK (risk_level IN ('low', 'medium', 'high'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_daily_fortune_profile_date ON daily_fortune(profile_id, fortune_date);
CREATE INDEX idx_daily_fortune_user_date ON daily_fortune(user_id, fortune_date);

-- =========================
-- 5. AI问答会话表
-- =========================
CREATE TABLE ai_chat_session (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    profile_id BIGINT NOT NULL,
    session_no VARCHAR(32) NOT NULL UNIQUE,
    session_date DATE NOT NULL,
    topic VARCHAR(64),
    context_scope VARCHAR(20) NOT NULL DEFAULT 'today',
    question_count INT NOT NULL DEFAULT 0,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    expires_at DATETIME,
    is_deleted TINYINT(1) NOT NULL DEFAULT 0,
    deleted_at DATETIME,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_ai_chat_session_user FOREIGN KEY (user_id) REFERENCES app_user(id),
    CONSTRAINT fk_ai_chat_session_profile FOREIGN KEY (profile_id) REFERENCES bazi_profile(id),
    CONSTRAINT chk_ai_chat_session_context_scope CHECK (context_scope IN ('today', 'recent', 'all')),
    CONSTRAINT chk_ai_chat_session_status CHECK (status IN ('active', 'closed', 'expired'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_ai_chat_session_user_date ON ai_chat_session(user_id, session_date);
CREATE INDEX idx_ai_chat_session_profile_date ON ai_chat_session(profile_id, session_date);

-- =========================
-- 6. AI问答消息表
-- =========================
CREATE TABLE ai_chat_message (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    session_id BIGINT NOT NULL,
    role_type VARCHAR(16) NOT NULL,
    question_category VARCHAR(64),
    content_text TEXT NOT NULL,
    content_masked TEXT,
    content_encrypted TEXT,
    risk_level VARCHAR(20) NOT NULL DEFAULT 'low',
    hit_sensitive_rule TINYINT(1) NOT NULL DEFAULT 0,
    refusal_type VARCHAR(32),
    review_status VARCHAR(20) NOT NULL DEFAULT 'approved',
    token_input INT,
    token_output INT,
    model_name VARCHAR(64),
    prompt_version VARCHAR(32),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_ai_chat_message_session FOREIGN KEY (session_id) REFERENCES ai_chat_session(id),
    CONSTRAINT chk_ai_chat_message_role CHECK (role_type IN ('user', 'assistant', 'system')),
    CONSTRAINT chk_ai_chat_message_risk_level CHECK (risk_level IN ('low', 'medium', 'high')),
    CONSTRAINT chk_ai_chat_message_review_status CHECK (review_status IN ('pending', 'approved', 'rejected'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_ai_chat_message_session ON ai_chat_message(session_id, id);
CREATE INDEX idx_ai_chat_message_category ON ai_chat_message(question_category);

-- =========================
-- 7. 提醒设置表
-- =========================
CREATE TABLE reminder_setting (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    channel_type VARCHAR(20) NOT NULL,
    reminder_time VARCHAR(8) NOT NULL DEFAULT '09:00',
    timezone VARCHAR(64) NOT NULL DEFAULT 'Asia/Shanghai',
    frequency_type VARCHAR(20) NOT NULL DEFAULT 'daily',
    is_enabled TINYINT(1) NOT NULL DEFAULT 1,
    quiet_days INT NOT NULL DEFAULT 0,
    last_sent_at DATETIME,
    is_deleted TINYINT(1) NOT NULL DEFAULT 0,
    deleted_at DATETIME,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT uk_reminder_setting UNIQUE (user_id, channel_type),
    CONSTRAINT fk_reminder_setting_user FOREIGN KEY (user_id) REFERENCES app_user(id),
    CONSTRAINT chk_reminder_setting_channel_type CHECK (channel_type IN ('in_app', 'subscribe_message', 'sms', 'wechat_template')),
    CONSTRAINT chk_reminder_setting_frequency_type CHECK (frequency_type IN ('daily', 'weekly', 'custom'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_reminder_setting_user_enabled ON reminder_setting(user_id, is_enabled);

-- =========================
-- 8. 提醒发送记录表
-- =========================
CREATE TABLE reminder_send_log (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    reminder_setting_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    channel_type VARCHAR(20) NOT NULL,
    plan_send_at DATETIME NOT NULL,
    actual_send_at DATETIME,
    send_status VARCHAR(20) NOT NULL DEFAULT 'pending',
    fail_reason VARCHAR(255),
    provider_message_id VARCHAR(128),
    retry_count INT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_reminder_send_log_setting FOREIGN KEY (reminder_setting_id) REFERENCES reminder_setting(id),
    CONSTRAINT fk_reminder_send_log_user FOREIGN KEY (user_id) REFERENCES app_user(id),
    CONSTRAINT chk_reminder_send_log_status CHECK (send_status IN ('pending', 'success', 'failed', 'cancelled'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_reminder_send_log_user_time ON reminder_send_log(user_id, plan_send_at);
CREATE INDEX idx_reminder_send_log_status ON reminder_send_log(send_status);

-- =========================
-- 9. 成长档案事件表
-- =========================
CREATE TABLE growth_archive_event (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    profile_id BIGINT,
    event_type VARCHAR(32) NOT NULL,
    event_date DATE NOT NULL,
    title VARCHAR(128) NOT NULL,
    content_text TEXT,
    ext_json JSON,
    source_type VARCHAR(32),
    is_deleted TINYINT(1) NOT NULL DEFAULT 0,
    deleted_at DATETIME,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_growth_archive_event_user FOREIGN KEY (user_id) REFERENCES app_user(id),
    CONSTRAINT fk_growth_archive_event_profile FOREIGN KEY (profile_id) REFERENCES bazi_profile(id),
    CONSTRAINT chk_growth_archive_event_type CHECK (event_type IN ('daily_fortune', 'qa_summary', 'weekly_summary', 'milestone'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_growth_archive_event_user_date ON growth_archive_event(user_id, event_date);

-- =========================
-- 10. 风控审核日志表
-- =========================
CREATE TABLE risk_audit_log (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    biz_type VARCHAR(32) NOT NULL,
    biz_id BIGINT NOT NULL,
    user_id BIGINT,
    risk_level VARCHAR(20) NOT NULL,
    rule_code VARCHAR(64),
    rule_name VARCHAR(128),
    hit_text TEXT,
    action_type VARCHAR(20) NOT NULL,
    audit_result VARCHAR(20) NOT NULL,
    reviewer VARCHAR(64),
    review_note VARCHAR(500),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_risk_audit_log_risk_level CHECK (risk_level IN ('low', 'medium', 'high')),
    CONSTRAINT chk_risk_audit_log_action_type CHECK (action_type IN ('pass', 'mask', 'reject', 'manual_review')),
    CONSTRAINT chk_risk_audit_log_audit_result CHECK (audit_result IN ('pending', 'approved', 'rejected'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_risk_audit_log_biz ON risk_audit_log(biz_type, biz_id);
CREATE INDEX idx_risk_audit_log_user ON risk_audit_log(user_id);

-- =========================
-- 11. 用户删数申请表
-- =========================
CREATE TABLE user_data_deletion_request (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    request_no VARCHAR(32) NOT NULL UNIQUE,
    request_status VARCHAR(20) NOT NULL DEFAULT 'pending',
    request_reason VARCHAR(255),
    submitted_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    approved_at DATETIME,
    executed_at DATETIME,
    execution_result VARCHAR(20),
    execution_note VARCHAR(500),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_data_deletion_request_user FOREIGN KEY (user_id) REFERENCES app_user(id),
    CONSTRAINT chk_user_data_deletion_request_status CHECK (request_status IN ('pending', 'approved', 'rejected', 'executed', 'failed')),
    CONSTRAINT chk_user_data_deletion_request_result CHECK (execution_result IS NULL OR execution_result IN ('success', 'partial_success', 'failed'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_user_data_deletion_request_user ON user_data_deletion_request(user_id);
CREATE INDEX idx_user_data_deletion_request_status ON user_data_deletion_request(request_status);

-- =========================
-- 12. 埋点事件表
-- =========================
CREATE TABLE tracking_event (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT,
    profile_id BIGINT,
    session_no VARCHAR(64),
    event_name VARCHAR(64) NOT NULL,
    event_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    page_name VARCHAR(64),
    device_type VARCHAR(32),
    platform_type VARCHAR(32),
    event_props JSON,
    is_sensitive TINYINT(1) NOT NULL DEFAULT 0,
    props_masked JSON,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_tracking_event_user FOREIGN KEY (user_id) REFERENCES app_user(id),
    CONSTRAINT fk_tracking_event_profile FOREIGN KEY (profile_id) REFERENCES bazi_profile(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_tracking_event_user_time ON tracking_event(user_id, event_time);
CREATE INDEX idx_tracking_event_name_time ON tracking_event(event_name, event_time);
