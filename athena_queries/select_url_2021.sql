SELECT
  CONCAT('s3://commoncrawl/', warc_filename) AS wet_file_s3_path,
  COUNT(*) AS url_count
FROM commoncrawl_cdx
WHERE
  crawl LIKE 'CC-MAIN-2021-%'
  AND url_host_registered_domain IN (
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
  AND NOT url LIKE '%robots.txt'
GROUP BY warc_filename
ORDER BY url_count DESC