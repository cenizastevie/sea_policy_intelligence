CREATE EXTERNAL TABLE IF NOT EXISTS sea_policy_intelligence.commoncrawl_cdx (
  url_surtkey                   STRING,
  url                           STRING,
  url_host_name                 STRING,
  url_host_tld                  STRING,
  url_host_2nd_last_part        STRING,
  url_host_3rd_last_part        STRING,
  url_host_4th_last_part        STRING,
  url_host_5th_last_part        STRING,
  url_host_registry_suffix      STRING,
  url_host_registered_domain    STRING,
  url_host_private_suffix       STRING,
  url_host_private_domain       STRING,
  url_protocol                  STRING,
  url_port                      INT,
  url_path                      STRING,
  url_query                     STRING,
  fetch_time                    TIMESTAMP,
  fetch_status                  SMALLINT,
  content_digest                STRING,
  content_mime_type             STRING,
  content_mime_detected         STRING,
  content_charset               STRING,
  content_languages             STRING,
  warc_filename                 STRING,
  warc_record_offset            INT,
  warc_record_length            INT,
  warc_segment                  STRING
)
PARTITIONED BY (
  crawl                         STRING,
  subset                        STRING
)
STORED AS parquet
LOCATION 's3://commoncrawl/cc-index/table/cc-main/warc/';