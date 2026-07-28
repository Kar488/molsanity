# RESULTS.md — validated numbers only

> Every number here is computed by code in this run and traceable to a
> logged artifact under `artifacts/`. No placeholders. See `LIMITATIONS.md`
> for caveats (notably: MUTAG ground truth is a chemically motivated
> nitro-motif *proxy*, not annotator labels).

## Audit matrix (dataset × backbone × attributor)

| dataset | backbone | attributor | split | n_mol | acc | gt_auroc | gt_auprc | motif_top1 | occ_spearman | occ_top1 | fid+ | fid- | sparsity | ece |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MUTAG | GINE | IntegratedGradients | scaffold | 20 | 0.600 | 0.218 | 0.159 | 0.981 | 0.576 | 0.800 | 0.271 | 0.270 | 0.770 | 0.323 |

### Metric legend
- **gt_auroc/gt_auprc**: attribution vs ground-truth motif mask (Tier-1 only; chance AUROC = 0.5). Below 0.5 means the attribution is *anti-aligned* with the known motif.
- **motif_top1**: fraction of attribution mass in the single top RDKit motif. **occ_spearman/occ_top1**: occlusion-vs-attribution faithfulness.
- **fid+/fid-**: Fidelity+ (prob drop removing salient atoms; higher is better) / Fidelity- (removing non-salient; lower is better). **ece**: test-set expected calibration error after temperature scaling.
