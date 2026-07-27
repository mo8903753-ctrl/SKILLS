# B2B→Consumer Claim Verification Checklist

When adapting a B2B/enterprise product for a Kickstarter consumer proposal, every spec claim from the product datasheet must be verified against three questions:

## Verification Questions

1. **Is this feature standard on the specific model being proposed, or is it optional/expansion?**
   - Example: 10GbE listed as "可选扩展槽" → must write "KS版需确认标配，当前资料为扩展槽选配"
   - Example: Docker/AI mentioned in series-level marketing but not in the specific model's datasheet → must write "需品牌方确认"

2. **Does the product have the certification this claim implies?**
   - Example: 3C certified but FCC/CE unconfirmed → must write "3C已具备 · FCC/CE需确认进度"
   - Never assume international certifications from domestic certifications

3. **Is the quantitative claim supported by the product materials?**
   - Example: "50+部署" when the materials show cases but no explicit count → must write "多行业政企客户" or ask brand for exact number
   - Example: "$5,000以下找不到第二个" → too absolute, soften to "$1,000级8盘位消费NAS价格带中，C2000具备少见的企业级数据保护配置"

4. **Is the technical configuration physically possible?**
   - Example: RAID-TP (triple-drive tolerance) with only 2 drives → impossible. RAID-TP requires ≥3 drives. 2-drive configs get RAID1/backup.
   - Example: "双端口冗余" on SAS when not all HDDs in a mixed SAS/SATA bay will have dual-port → split into separate claims: "12Gb SAS高速通道 · 支持SAS/SATA/SSD硬盘"

5. **Are market statistics accurate and sourced?**
   - Example: US 60% + EU 28% + AP 18% = 106% → impossible. Delete percentages, use qualitative ranking.
   - Example: Any percentage claim without a source → add source line or remove the number

6. **Is the sample count consistent across the document?**
   - Example: "1台预产样机" in one section but "5-6位KOL" in another → must unify: "至少5台评测样机 + 1台拍摄备机"

## Claims That Survived Verification (C2000 case study)

These claims passed all six verification questions against the product datasheets:
- 8盘位塔式桌面NAS
- RAID-TP 三盘容错
- 静默错误自动修复
- WORM 防篡改
- 审计日志
- RECC 纠错内存
- BMC 服务器管理芯片
- 双系统盘冗余
- SAS/SATA/SSD 硬盘支持
- 13级权限细分
- PC自动备份客户端

## Claims That Required Modification (C2000 case study)

| Original claim | Problem | Fixed version |
|---------------|---------|---------------|
| 10/25GbE标配 | 资料写"标配2×1GbE，可选扩展" | KS版需确认标配，当前为扩展槽选配 |
| Docker + AI算力 | C2000-D单页无此功能，出现在系列/存算一体语境 | 支持容器扩展能力需品牌方确认；AI加速卡仅作Stretch Goal |
| 2×8TB RAID-TP | RAID-TP需要≥3盘 | 2×8TB：RAID1/备份；4×/8×8TB：可选RAID-TP |
| 零遥测、零账号、零中间人 | 资料未证明零云端连接 | 可本地部署，不依赖公有云账号 |
| 50+政企部署 | 资料有案例但无明确"50+"数字 | 多行业政企客户（法院/医院/大学/铁路等） |
| FCC/CE认证已具备 | 资料仅明确3C认证 | 3C已具备 · FCC/CE需确认进度 |
| US 60% + EU 28% + AP 18% | 总和106%，来源不明 | 删百分比，用定性优先级描述 |
| 1台预产样机 | 与KOL数量矛盾 | 至少5台评测样机 + 1台拍摄备机 |

## Pitfall: RAID-TP Drive Count

RAID-TP requires ≥3 data drives. Writing "2×8TB 企业盘 · 预配RAID-TP" is physically wrong and will be caught by any technically literate reviewer. Always verify the drive count against the RAID level:
- 2 drives → RAID1 or backup/sync only
- 4+ drives → RAID-TP / RAID5 / RAID6 are options
- 8 drives → full RAID-TP configuration possible
