# Test filings

Annual reports used to build and test ingestion. All are public filings of the companies named.

## Used while the pipeline was built

The location, extraction and comparison stages were developed against these six, so passing on them
says little about other reports. All six come from EDGAR's PDF service.

| File | Pages | PDF producer | SHA-256 |
|---|---|---|---|
| `meta/meta-10k-2024.pdf` | 150 | EDGAR's PDF service | `be49f4b35fc1e04ef48562c4c93763d00f316d8002cf7adbe7fb6d3aff6d64b9` |
| `meta/meta-10k-2025.pdf` | 145 | EDGAR's PDF service | `457ef30095d64b668da6e00ac2b3f4142f2fa1c201497f46b645491a78cb273f` |
| `oracle/oracle-10k-2025.pdf` | 118 | EDGAR's PDF service | `d6d3899b0a11b89f9aac1659933b782bc7bc47ccc98713e914934806abd5a6e7` |
| `oracle/oracle-10k-2026.pdf` | 139 | EDGAR's PDF service | `27ca3281e092890a8744e2307460a8b7397da1ff6371fae21a1d0d84e514b592` |
| `snowflake/snowflake-10k-2025.pdf` | 229 | EDGAR's PDF service | `1121645fa072542aa5f88792826c42adcfc8599a15ee811ffc7219eb1c9a1d47` |
| `snowflake/snowflake-10k-2026.pdf` | 208 | EDGAR's PDF service | `6851f61cf7b2a2c804b1baeafdc98f1430b1ae7e89ecf42e65598684e9815a86` |

## First run after the pipeline was finished

Added on 2026-11-18 to test whether the pipeline holds on reports it was not built against: other
companies, and PDFs from three other producers. The four in the first table were run with the pipeline
frozen, and what failed on them was fixed with general rules. The three in the second table were
then run once, untouched until that run. The results of both runs are in the ingestion plan.

Downloaded from the companies' investor relations sites:

| File | Pages | PDF producer | SHA-256 | Source |
|---|---|---|---|---|
| `apple/apple-10k-2024.pdf` | 121 | Workiva | `319e1217afe72f194575e63350ea6c813eaf5caf0c24e59ce8b221fc1b3ea0d4` | https://s2.q4cdn.com/470004039/files/doc_earnings/2024/q4/filing/10-Q4-2024-As-Filed.pdf |
| `amazon/amazon-ar-2024.pdf` | 91 | Adobe InDesign | `d6c8919af431fbf38d5d92f2060ba8f45d084f26495c6f17ce81232102977908` | https://s2.q4cdn.com/299287126/files/doc_financials/2025/ar/Amazon-2024-Annual-Report.pdf |
| `amd/amd-10k-2024.pdf` | 138 | Equisolve | `079208174889130f5d6696d1199869b3e8f49d7a879473d040c069ffc9620491` | https://ir.amd.com/financial-information/sec-filings/content/0000002488-25-000012/0000002488-25-000012.pdf |
| `netflix/netflix-10k-2024.pdf` | 84 | EDGAR's PDF service | `a8a00a029bddb45fa83d151798a9c4c94b8725c9a0a1ee490e2e7da8ec1e9ddb` | https://s22.q4cdn.com/959853165/files/doc_financials/2024/ar/Netflix-10-K-01272025.pdf |

Run once, untouched until then:

| File | Pages | PDF producer | SHA-256 | Source |
|---|---|---|---|---|
| `palantir/palantir-10k-2024.pdf` | 145 | Workiva | `d525792fef879690ce3d052eea1540047127572b8b31fad6678cf39fbb4703b8` | https://investors.palantir.com/files/2024%20FY%20PLTR%2010-K.pdf |
| `intel/intel-10k-2024.pdf` | 270 | Equisolve | `a4d3952ee70acb8f51debc09adc0c5cde57446cfac061ed57398fbac72de8023` | https://www.intc.com/filings-reports/all-sec-filings/content/0000050863-25-000009/0000050863-25-000009.pdf |
| `nvidia/nvidia-10k-2025.pdf` | 130 | EDGAR's PDF service | `b67bd67a64488a54886de001c788bc5059a965fc6ef5b4d8b71624951e13df8e` | https://s201.q4cdn.com/141608511/files/doc_financials/2025/q4/177440d5-3b32-4185-8cc8-95500a9dc783.pdf |

Amazon's file is its designed annual report, which contains the 10-K; the others are the 10-K as filed.

## Two copies of one filing

Added on 2026-11-20 to test whether a different layout of the same filing changes the result. Ten
companies not in the set before, each with its latest 10-K in two copies: one rendered from the
filing's HTML on EDGAR by `scripts/download_annual_reports.py` and `scripts/render_annual_reports.js`
(also listed in `sources.csv`), and one PDF from the company's investor relations site, named with
`-ir`. Neither copy had been run through the pipeline when they were added.

| File | Pages | PDF producer | SHA-256 | Source |
|---|---|---|---|---|
| `airbnb/airbnb-10k-2025.pdf` | 154 | Chromium (our render) | `85a8966ecc00b9fcdc55ca4c53d44bad035823b78a19528b81117c8b4f6c5a83` | https://www.sec.gov/Archives/edgar/data/1559720/000155972026000004/abnb-20251231.htm |
| `airbnb/airbnb-10k-2025-ir.pdf` | 94 | EDGAR's PDF service | `48a78febd054e9a1e8b58207a6f7bf38eb7a2691cfab4acf5b173941c49c3e92` | https://d18rn0p25nwr6d.cloudfront.net/CIK-0001559720/52fc9020-faa3-4ed3-b6e3-9a982ecdda93.pdf |
| `alphabet/alphabet-10k-2025.pdf` | 163 | Chromium (our render) | `a9fb45a52f7c4a41e6c3ea7c8ebac6d6ac5996ff22a1b55bc69130977ec7943c` | https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm |
| `alphabet/alphabet-10k-2025-ir.pdf` | 99 | Workiva | `9953e8d2e70b18c5bf0af3b2b2a1e96de0555f51cbb39a625497b434e19fb43a` | https://s206.q4cdn.com/479360582/files/doc_financials/2025/q4/GOOG-10-K-2025.pdf |
| `broadcom/broadcom-10k-2025.pdf` | 164 | Chromium (our render) | `ea9af87181c24f9273c1fdb0e4a030905927cff7235bfd53f136b18c6052a91a` | https://www.sec.gov/Archives/edgar/data/1730168/000173016825000121/avgo-20251102.htm |
| `broadcom/broadcom-10k-2025-ir.pdf` | 113 | KS PDF Engine (Chromium) | `eeab6d8de58086992fb302ad6e5f7ec6f453e2c754c38a6e17a2a99fceeb1a17` | https://investors.broadcom.com/static-files/5868c796-2455-4855-9f02-3410b11e99e1 |
| `cisco/cisco-10k-2026.pdf` | 175 | Chromium (our render) | `6a4d1d15691ed36371289466971129668a8e235440b7e576997acf673ef6b211` | https://www.sec.gov/Archives/edgar/data/858877/000085887726000132/csco-20260725.htm |
| `cisco/cisco-10k-2026-ir.pdf` | 285 | EDGAR's PDF service | `1a02d7787ab8bbe822f22932f1b2e7f960c94d12666232dd07009447f7d9a36e` | https://s21.q4cdn.com/812015656/files/doc_financials/2026/q4/028fbac9-c5ba-409b-83ce-dfee9c17fdbc.pdf |
| `fortinet/fortinet-10k-2025.pdf` | 220 | Chromium (our render) | `416247c8b7beb643fa8dd6d78156affaf12aa4fa4a34e0a987c5072ea75e5b26` | https://www.sec.gov/Archives/edgar/data/1262039/000126203926000007/ftnt-20251231.htm |
| `fortinet/fortinet-10k-2025-ir.pdf` | 139 | KS PDF Engine (Chromium) | `7fb10efaf13941d5636aa475f4fa1690883d63efa3968399140b471c204475c9` | https://investor.fortinet.com/static-files/7058aea1-a50c-4b7b-905f-ba5aedb92f40 |
| `micron/micron-10k-2026.pdf` | 175 | Chromium (our render) | `7ec028ce829e95bc8dc6f562a3a7ee3e9cab3ae085bd8abdad41878d4e59941a` | https://www.sec.gov/Archives/edgar/data/723125/000072312526000023/mu-20260903.htm |
| `micron/micron-10k-2026-ir.pdf` | 381 | EDGAR's PDF service | `aa227d7af0003b3ead47c7b6bb628b98668c8065d14a917d734b2638185b48b3` | https://d18rn0p25nwr6d.cloudfront.net/CIK-0000723125/5dafce68-38e8-4cad-a8f3-ab56d04d73fd.pdf |
| `paypal/paypal-10k-2025.pdf` | 202 | Chromium (our render) | `d32ac181fdc4b796e76fd3ae663c558c4ed88acd75563ce5e328da3fbda5ce55` | https://www.sec.gov/Archives/edgar/data/1633917/000163391726000024/pypl-20251231.htm |
| `paypal/paypal-10k-2025-ir.pdf` | 443 | EDGAR's PDF service | `03dbd163eb5cc37ab6eaaa17e840bdc940edb7d4c85d2c43e701afd1c26047c0` | https://s205.q4cdn.com/875401827/files/doc_financials/2025/q4/10-K.pdf |
| `qualcomm/qualcomm-10k-2026.pdf` | 137 | Chromium (our render) | `e1c9f7f6711277db13a893651fefa51b91e6815ea86a24be8a49256f963a88bd` | https://www.sec.gov/Archives/edgar/data/804328/000080432826000128/qcom-20260927.htm |
| `qualcomm/qualcomm-10k-2026-ir.pdf` | 82 | Workiva | `8ef082979b9f81b5e7a891e87393d2145ff789958d4d561249d7c5a1f0df7689` | https://s204.q4cdn.com/645488518/files/content_files/QCOM-09-27-26-10-K_Final-v2-IR.pdf |
| `texas-instruments/texas-instruments-10k-2025.pdf` | 106 | Chromium (our render) | `ffbc7e05bd84806a2539ff7db03f972f8a8c03d639da8b1ac5b1d9c67d8384d1` | https://www.sec.gov/Archives/edgar/data/97476/000009747626000059/txn-20251231.htm |
| `texas-instruments/texas-instruments-10k-2025-ir.pdf` | 78 | KS PDF Engine (Chromium) | `fb18301ce87cf7304669835b76e07408284fad47dc4910b46cccd18139236fc5` | https://investor.ti.com/static-files/7a676084-0b6d-479d-80bb-b193f27135f4 |
| `uber/uber-10k-2025.pdf` | 222 | Chromium (our render) | `70fef9c552539219f107fdbdd628b8436336a1e1a1fd66102831175b5a5b1e6d` | https://www.sec.gov/Archives/edgar/data/1543151/000154315126000015/uber-20251231.htm |
| `uber/uber-10k-2025-ir.pdf` | 149 | EDGAR's PDF service | `6e4603267ea61dc39a9a6c63e2b261660854db4fc04fd3b7fa1c719aaf732051` | https://d18rn0p25nwr6d.cloudfront.net/CIK-0001543151/22e9f27b-deea-485f-b5b6-7ecc7462b84a.pdf |

Every company copy is the 10-K as filed. The ones on `d18rn0p25nwr6d.cloudfront.net` are served from
the filings store of the IR provider the companies use (Q4), under each company's CIK. Cisco's,
Micron's and PayPal's copies include every exhibit: the 10-K itself ends with its signatures on pages
105, 104 and 124. Broadcom's, Fortinet's and Texas Instruments' sites refuse automated downloads, so
their copies were saved in a browser.
