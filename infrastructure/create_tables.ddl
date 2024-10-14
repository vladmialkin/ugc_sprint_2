CREATE TABLE IF NOT EXISTS default.click (
        event_type String,
        user_id String,
        element_id String,
        created_at String,
        PRIMARY KEY (user_id, created_at)
    ) ENGINE = MergeTree()
    ORDER BY (user_id, created_at);

CREATE TABLE IF NOT EXISTS default.page_view (
    event_type String,
    user_id String,
    page_id String,
    element_id String,
    element_info String,
    created_at String,
    PRIMARY KEY (user_id, created_at)
) ENGINE = MergeTree()
ORDER BY (user_id, created_at);

CREATE TABLE IF NOT EXISTS default.time_on_page (
    event_type String,
    user_id String,
    element_id String,
    element_info String,
    duration Int32,
    created_at String,
    PRIMARY KEY (user_id, created_at)
) ENGINE = MergeTree()
ORDER BY (user_id, created_at);

CREATE TABLE IF NOT EXISTS default.change_video_quality (
    event_type String,
    user_id String,
    video_id String,
    quality_before Int32,
    quality_after Int32,
    created_at String,
    PRIMARY KEY (user_id, created_at)
) ENGINE = MergeTree()
ORDER BY (user_id, created_at);

CREATE TABLE IF NOT EXISTS default.watch_to_the_end (
    event_type String,
    user_id String,
    video_id String,
    duration Int32,
    viewed Int32,
    created_at String,
    PRIMARY KEY (user_id, created_at)
) ENGINE = MergeTree()
ORDER BY (user_id, created_at);

CREATE TABLE IF NOT EXISTS default.using_search_filters (
    event_type String,
    user_id String,
    filters String,
    created_at String,
    PRIMARY KEY (user_id, created_at)
) ENGINE = MergeTree()
ORDER BY (user_id, created_at);

