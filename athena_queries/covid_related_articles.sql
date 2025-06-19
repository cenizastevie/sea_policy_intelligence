SELECT
  CONCAT('s3://commoncrawl/', warc_filename) AS wet_file_s3_path,
  url
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
  AND (
    -- Covid, health, and policy-related keywords
    url LIKE '%pandemic%' OR url LIKE '%coronavirus%' OR url LIKE '%covid19%' OR url LIKE '%sarscov2%' OR
    url LIKE '%lockdown%' OR url LIKE '%quarantine%' OR url LIKE '%distancing%' OR url LIKE '%flatten%' OR
    url LIKE '%tracing%' OR url LIKE '%vaccine%' OR url LIKE '%vaccination%' OR url LIKE '%immunity%' OR
    url LIKE '%mask%' OR url LIKE '%testing%' OR url LIKE '%isolation%' OR url LIKE '%transmission%' OR
    url LIKE '%asymptomatic%' OR url LIKE '%fatality%' OR url LIKE '%epidemic%' OR url LIKE '%outbreak%' OR
    url LIKE '%infection%' OR url LIKE '%ppe%' OR url LIKE '%ventilator%' OR url LIKE '%telehealth%' OR
    url LIKE '%authorization%' OR url LIKE '%restrictions%' OR url LIKE '%essential%' OR url LIKE '%remote%' OR
    url LIKE '%closure%' OR url LIKE '%relief%' OR url LIKE '%stimulus%' OR url LIKE '%policy%' OR
    url LIKE '%healthcare%' OR url LIKE '%epidemiology%' OR url LIKE '%mutation%' OR url LIKE '%variant%' OR
    url LIKE '%booster%' OR url LIKE '%longcovid%' OR url LIKE '%equity%' OR url LIKE '%wellness%' OR
    url LIKE '%prevention%' OR url LIKE '%screening%' OR url LIKE '%treatment%' OR url LIKE '%symptoms%' OR
    url LIKE '%hospitalization%' OR url LIKE '%recovery%' OR url LIKE '%immunization%' OR url LIKE '%antibody%' OR
    url LIKE '%dose%' OR url LIKE '%sideeffects%' OR url LIKE '%government%' OR url LIKE '%regulation%' OR
    url LIKE '%guidelines%' OR url LIKE '%mandate%' OR url LIKE '%compliance%' OR url LIKE '%enforcement%' OR
    url LIKE '%cases%' OR url LIKE '%surge%' OR url LIKE '%reporting%' OR url LIKE '%statistics%' OR
    url LIKE '%monitoring%' OR url LIKE '%containment%' OR url LIKE '%response%' OR url LIKE '%preparedness%' OR
    url LIKE '%publicservice%' OR url LIKE '%health%' OR url LIKE '%wellbeing%' OR url LIKE '%sanitizer%' OR
    url LIKE '%handwashing%' OR url LIKE '%outpatient%' OR url LIKE '%inpatient%' OR url LIKE '%triage%' OR
    url LIKE '%icu%' OR url LIKE '%ventilation%' OR url LIKE '%mortality%' OR url LIKE '%morbidity%' OR
    url LIKE '%cluster%' OR url LIKE '%spread%' OR url LIKE '%contact%' OR url LIKE '%exposure%' OR
    url LIKE '%risk%' OR url LIKE '%susceptibility%' OR url LIKE '%carrier%' OR url LIKE '%testingkit%' OR
    url LIKE '%swab%' OR url LIKE '%positivity%' OR url LIKE '%negativity%' OR url LIKE '%screen%' OR
    url LIKE '%trace%' OR url LIKE '%quarantineorder%' OR url LIKE '%curfew%' OR url LIKE '%shutdown%' OR
    url LIKE '%reopen%' OR url LIKE '%recoveryrate%' OR url LIKE '%deathrate%' OR url LIKE '%symptomatic%' OR
    url LIKE '%presymptomatic%' OR url LIKE '%postacute%' OR url LIKE '%fatigue%' OR url LIKE '%cough%' OR
    url LIKE '%fever%' OR url LIKE '%shortness%' OR url LIKE '%breath%' OR url LIKE '%loss%' OR
    url LIKE '%taste%' OR url LIKE '%smell%' OR url LIKE '%myalgia%' OR url LIKE '%headache%' OR
    url LIKE '%chills%' OR url LIKE '%sorethroat%' OR url LIKE '%congestion%' OR url LIKE '%nausea%' OR
    url LIKE '%vomiting%' OR url LIKE '%diarrhea%' OR url LIKE '%outreach%' OR url LIKE '%awareness%' OR
    url LIKE '%campaign%' OR url LIKE '%education%' OR url LIKE '%messaging%' OR url LIKE '%communication%' OR
    url LIKE '%misinformation%' OR url LIKE '%disinformation%' OR url LIKE '%infodemic%' OR url LIKE '%hotspot%' OR
    url LIKE '%redzone%' OR url LIKE '%containmentzone%' OR url LIKE '%contactless%' OR url LIKE '%telemedicine%' OR
    url LIKE '%virtualcare%' OR url LIKE '%homecare%' OR url LIKE '%selfisolation%' OR url LIKE '%selfquarantine%' OR
    url LIKE '%screeningcenter%' OR url LIKE '%testingcenter%' OR url LIKE '%drivein%' OR url LIKE '%walkin%' OR
    url LIKE '%massgathering%' OR url LIKE '%eventban%' OR url LIKE '%travelban%' OR url LIKE '%bordercontrol%' OR
    url LIKE '%entryscreening%' OR url LIKE '%exitcontrol%' OR url LIKE '%passport%' OR url LIKE '%certificate%' OR
    url LIKE '%immunitypassport%' OR url LIKE '%digitalhealth%' OR url LIKE '%app%' OR url LIKE '%exposurealert%' OR
    url LIKE '%notification%' OR url LIKE '%surveillance%' OR url LIKE '%genome%' OR url LIKE '%sequencing%' OR
    url LIKE '%mutationtracking%' OR url LIKE '%variantofconcern%' OR url LIKE '%variantofinterest%' OR
    url LIKE '%boosterdose%' OR url LIKE '%thirdshot%' OR url LIKE '%fourthdose%' OR url LIKE '%waningimmunity%' OR
    url LIKE '%breakthrough%' OR url LIKE '%reinfection%' OR url LIKE '%herdimmunity%' OR url LIKE '%communityspread%' OR
    url LIKE '%clusteroutbreak%' OR url LIKE '%supercluster%' OR url LIKE '%superspreader%' OR url LIKE '%event%' OR
    url LIKE '%essentialworker%' OR url LIKE '%frontline%' OR url LIKE '%healthworker%' OR url LIKE '%doctor%' OR
    url LIKE '%nurse%' OR url LIKE '%paramedic%' OR url LIKE '%pharmacist%' OR url LIKE '%volunteer%' OR
    url LIKE '%publichealth%' OR url LIKE '%policychange%' OR url LIKE '%executiveorder%' OR url LIKE '%legislation%' OR
    url LIKE '%ordinance%' OR url LIKE '%taskforce%' OR url LIKE '%committee%' OR url LIKE '%advisory%' OR
    url LIKE '%briefing%' OR url LIKE '%pressrelease%' OR url LIKE '%publicnotice%' OR url LIKE '%emergency%' OR
    url LIKE '%stateofemergency%' OR url LIKE '%disaster%' OR url LIKE '%reliefaid%' OR url LIKE '%funding%' OR
    url LIKE '%grant%' OR url LIKE '%allocation%' OR url LIKE '%distribution%' OR url LIKE '%logistics%' OR
    url LIKE '%supplychain%' OR url LIKE '%stockpile%' OR url LIKE '%rationing%' OR url LIKE '%shortage%' OR
    url LIKE '%surplus%' OR url LIKE '%donation%' OR url LIKE '%aid%' OR url LIKE '%international%' OR
    url LIKE '%cooperation%' OR url LIKE '%partnership%' OR url LIKE '%collaboration%' OR url LIKE '%research%' OR
    url LIKE '%trial%' OR url LIKE '%clinicaltrial%' OR url LIKE '%approval%' OR url LIKE '%rollout%' OR
    url LIKE '%deployment%' OR url LIKE '%uptake%' OR url LIKE '%hesitancy%' OR url LIKE '%acceptance%' OR
    url LIKE '%coverage%' OR url LIKE '%access%' OR url LIKE '%availability%' OR url LIKE '%affordability%' OR
    url LIKE '%insurance%' OR url LIKE '%copay%' OR url LIKE '%subsidy%' OR url LIKE '%assistance%' OR url LIKE '%support%'
  )
ORDER BY warc_filename, url