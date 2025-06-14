-- Athena query to search Common Crawl for Southeast Asian news outlets and policy keywords (past 6 months)
-- Update the 'crawl' list with the latest 6 crawl names from https://commoncrawl.org/the-data/get-started/

SELECT url, fetch_time
FROM commoncrawl_cdx
WHERE
  crawl IN (
    'CC-MAIN-2025-22',
    'CC-MAIN-2025-18',
    'CC-MAIN-2025-14',
    'CC-MAIN-2025-10',
    'CC-MAIN-2025-06',
    'CC-MAIN-2025-02'
  )
  AND (
    url_host_registered_domain IN (
      'pna.gov.ph', 'news.abs-cbn.com', 'gmanetwork.com', 'philstar.com', 'inquirer.net',
      'antaranews.com', 'thejakartapost.com', 'kompas.com', 'detik.com',
      'bernama.com', 'thestar.com.my', 'nst.com.my', 'malaymail.com',
      'straitstimes.com', 'channelnewsasia.com', 'todayonline.com',
      'bangkokpost.com', 'nationthailand.com', 'thaipbsworld.com',
      'vnanet.vn', 'e.vnexpress.net', 'vietnamnews.vn',
      'gnlm.com.mm', 'mmtimes.com', 'elevenmyanmar.com',
      'khmertimeskh.com', 'phnompenhpost.com', 'akp.gov.kh',
      'kpl.gov.la', 'vientianetimes.org.la',
      'borneobulletin.com.bn', 'rtbnews.rtb.gov.bn'
    )
  )
  AND (
    LOWER(url) LIKE '%education%' OR
    LOWER(url) LIKE '%health%' OR
    LOWER(url) LIKE '%infrastructure%' OR
    LOWER(url) LIKE '%transportation%' OR
    LOWER(url) LIKE '%housing%' OR
    LOWER(url) LIKE '%agriculture%' OR
    LOWER(url) LIKE '%defense%' OR
    LOWER(url) LIKE '%foreign policy%' OR
    LOWER(url) LIKE '%taxation%' OR
    LOWER(url) LIKE '%budget%' OR
    LOWER(url) LIKE '%energy%' OR
    LOWER(url) LIKE '%environment%' OR
    LOWER(url) LIKE '%justice%' OR
    LOWER(url) LIKE '%public safety%' OR
    LOWER(url) LIKE '%employment%' OR
    LOWER(url) LIKE '%poverty%' OR
    LOWER(url) LIKE '%climate change%' OR
    LOWER(url) LIKE '%digital transformation%' OR
    LOWER(url) LIKE '%public administration%' OR
    LOWER(url) LIKE '%corruption%' OR
    LOWER(url) LIKE '%disaster response%' OR
    LOWER(url) LIKE '%social welfare%' OR
    LOWER(url) LIKE '%urban development%' OR
    LOWER(url) LIKE '%rural development%' OR
    LOWER(url) LIKE '%immigration%' OR
    LOWER(url) LIKE '%trade%' OR
    LOWER(url) LIKE '%tourism%' OR
    LOWER(url) LIKE '%technology%' OR
    LOWER(url) LIKE '%women''s rights%' OR
    LOWER(url) LIKE '%labor rights%' OR
    LOWER(url) LIKE '%human rights%' OR
    LOWER(url) LIKE '%elections%' OR
    LOWER(url) LIKE '%governance%' OR
    LOWER(url) LIKE '%constitution%' OR
    LOWER(url) LIKE '%inclusivity%' OR
    LOWER(url) LIKE '%youth development%' OR
    LOWER(url) LIKE '%public finance%' OR
    LOWER(url) LIKE '%policy reform%' OR
    LOWER(url) LIKE '%law enforcement%'
  )
LIMIT 1000;
