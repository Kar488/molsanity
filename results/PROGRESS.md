# PROGRESS.md — MolSanity rolling progress

_Last run: `full.yaml` @ 20260730_164248._

## Cell tally

- done: **59**  · failed: **27**  · skipped/blocked: **2**

## Cells (dataset × backbone × attributor)

| dataset | backbone | attributor | status | detail |
| --- | --- | --- | --- | --- |
| SynthMotifs | GINE | IntegratedGradients | done | acc=0.95 gt_auroc=0.9011999999999999 n=20 (capped) [cached] |
| SynthMotifs | GINE | IntegratedGradients | done | acc=1.00 gt_auroc=0.998 n=20 (capped) [cached] |
| SynthMotifs | GINE | Saliency | done | acc=0.95 gt_auroc=0.9752000000000001 n=20 (capped) [cached] |
| SynthMotifs | GINE | Saliency | done | acc=1.00 gt_auroc=0.9992000000000001 n=20 (capped) [cached] |
| SynthMotifs | GINE | InputXGradient | done | acc=0.95 gt_auroc=0.9683999999999999 n=20 (capped) [cached] |
| SynthMotifs | GINE | InputXGradient | done | acc=1.00 gt_auroc=0.9916 n=20 (capped) [cached] |
| SynthMotifs | GINE | GuidedBackprop | done | acc=0.95 gt_auroc=0.9279999999999999 n=20 (capped) [cached] |
| SynthMotifs | GINE | GuidedBackprop | done | acc=1.00 gt_auroc=1.0 n=20 (capped) [cached] |
| SynthMotifs | GINE | GNNExplainer | done | acc=0.95 gt_auroc=0.6680000000000001 n=20 (capped) [cached] |
| SynthMotifs | GINE | GNNExplainer | done | acc=1.00 gt_auroc=0.4744 n=20 (capped) [cached] |
| SynthMotifs | GINE | PGExplainer | failed | Expected all tensors to be on the same device, but got mat1 is on cuda:0, different from other tensors on cpu (when checking argument in method wrapper_CUDA_addmm) (see logs/error_SynthMotifs__GINE__PGExplainer__scaffold_20260730_164248.log) |
| SynthMotifs | GINE | PGExplainer | failed | Expected all tensors to be on the same device, but got mat1 is on cuda:0, different from other tensors on cpu (when checking argument in method wrapper_CUDA_addmm) (see logs/error_SynthMotifs__GINE__PGExplainer__random_20260730_164248.log) |
| SynthMotifs | GCN | IntegratedGradients | done | acc=0.70 gt_auroc=0.9867999999999999 n=20 (capped) [cached] |
| SynthMotifs | GCN | IntegratedGradients | done | acc=0.60 gt_auroc=0.4796 n=20 (capped) [cached] |
| SynthMotifs | GAT | IntegratedGradients | done | acc=0.95 gt_auroc=0.5916 n=20 (capped) [cached] |
| SynthMotifs | GAT | IntegratedGradients | done | acc=1.00 gt_auroc=0.8739999999999999 n=20 (capped) [cached] |
| SynthMotifs | MPNN | IntegratedGradients | done | acc=0.65 gt_auroc=0.7116 n=20 (capped) [cached] |
| SynthMotifs | MPNN | IntegratedGradients | done | acc=1.00 gt_auroc=0.8388 n=20 (capped) [cached] |
| SynthMotifs | AttentiveFP | IntegratedGradients | done | acc=0.85 gt_auroc=0.8856000000000002 n=20 (capped) [cached] |
| SynthMotifs | AttentiveFP | IntegratedGradients | done | acc=1.00 gt_auroc=0.7156 n=20 (capped) [cached] |
| MUTAG | GINE | IntegratedGradients | failed | can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first. (see logs/error_MUTAG__GINE__IntegratedGradients__scaffold_20260730_164248.log) |
| MUTAG | GINE | IntegratedGradients | failed | can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first. (see logs/error_MUTAG__GINE__IntegratedGradients__random_20260730_164248.log) |
| MUTAG | GINE | Saliency | failed | can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first. (see logs/error_MUTAG__GINE__Saliency__scaffold_20260730_164248.log) |
| MUTAG | GINE | Saliency | failed | can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first. (see logs/error_MUTAG__GINE__Saliency__random_20260730_164248.log) |
| MUTAG | GINE | InputXGradient | failed | can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first. (see logs/error_MUTAG__GINE__InputXGradient__scaffold_20260730_164248.log) |
| MUTAG | GINE | InputXGradient | failed | can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first. (see logs/error_MUTAG__GINE__InputXGradient__random_20260730_164248.log) |
| MUTAG | GINE | GuidedBackprop | failed | can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first. (see logs/error_MUTAG__GINE__GuidedBackprop__scaffold_20260730_164248.log) |
| MUTAG | GINE | GuidedBackprop | failed | can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first. (see logs/error_MUTAG__GINE__GuidedBackprop__random_20260730_164248.log) |
| MUTAG | GINE | GNNExplainer | failed | can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first. (see logs/error_MUTAG__GINE__GNNExplainer__scaffold_20260730_164248.log) |
| MUTAG | GINE | GNNExplainer | failed | can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first. (see logs/error_MUTAG__GINE__GNNExplainer__random_20260730_164248.log) |
| MUTAG | GINE | PGExplainer | failed | Expected all tensors to be on the same device, but got mat1 is on cuda:0, different from other tensors on cpu (when checking argument in method wrapper_CUDA_addmm) (see logs/error_MUTAG__GINE__PGExplainer__scaffold_20260730_164248.log) |
| MUTAG | GINE | PGExplainer | failed | Expected all tensors to be on the same device, but got mat1 is on cuda:0, different from other tensors on cpu (when checking argument in method wrapper_CUDA_addmm) (see logs/error_MUTAG__GINE__PGExplainer__random_20260730_164248.log) |
| MUTAG | GCN | IntegratedGradients | failed | can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first. (see logs/error_MUTAG__GCN__IntegratedGradients__scaffold_20260730_164248.log) |
| MUTAG | GCN | IntegratedGradients | failed | can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first. (see logs/error_MUTAG__GCN__IntegratedGradients__random_20260730_164248.log) |
| MUTAG | GAT | IntegratedGradients | failed | can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first. (see logs/error_MUTAG__GAT__IntegratedGradients__scaffold_20260730_164248.log) |
| MUTAG | GAT | IntegratedGradients | failed | can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first. (see logs/error_MUTAG__GAT__IntegratedGradients__random_20260730_164248.log) |
| MUTAG | MPNN | IntegratedGradients | failed | can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first. (see logs/error_MUTAG__MPNN__IntegratedGradients__scaffold_20260730_164248.log) |
| MUTAG | MPNN | IntegratedGradients | failed | can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first. (see logs/error_MUTAG__MPNN__IntegratedGradients__random_20260730_164248.log) |
| MUTAG | AttentiveFP | IntegratedGradients | failed | can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first. (see logs/error_MUTAG__AttentiveFP__IntegratedGradients__scaffold_20260730_164248.log) |
| MUTAG | AttentiveFP | IntegratedGradients | failed | can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first. (see logs/error_MUTAG__AttentiveFP__IntegratedGradients__random_20260730_164248.log) |
| BBBP | GINE | IntegratedGradients | done | acc=0.95 gt_auroc=nan n=100 (capped) [cached] |
| BBBP | GINE | IntegratedGradients | done | acc=0.82 gt_auroc=nan n=100 (capped) [cached] |
| BBBP | GCN | IntegratedGradients | done | acc=0.98 gt_auroc=nan n=100 (capped) [cached] |
| BBBP | GCN | IntegratedGradients | done | acc=0.79 gt_auroc=nan n=100 (capped) [cached] |
| BBBP | GAT | IntegratedGradients | done | acc=0.98 gt_auroc=nan n=100 (capped) [cached] |
| BBBP | GAT | IntegratedGradients | done | acc=0.78 gt_auroc=nan n=100 (capped) [cached] |
| BBBP | MPNN | IntegratedGradients | done | acc=0.95 gt_auroc=nan n=100 (capped) [cached] |
| BBBP | MPNN | IntegratedGradients | done | acc=0.84 gt_auroc=nan n=100 (capped) [cached] |
| BBBP | AttentiveFP | IntegratedGradients | done | acc=0.95 gt_auroc=nan n=100 (capped) [cached] |
| BBBP | AttentiveFP | IntegratedGradients | done | acc=0.77 gt_auroc=nan n=100 (capped) [cached] |
| BBBP | GINE | GNNExplainer | done | acc=0.95 gt_auroc=nan n=100 (capped) [cached] |
| BBBP | GINE | GNNExplainer | done | acc=0.82 gt_auroc=nan n=100 (capped) [cached] |
| BBBP | GINE | PGExplainer | failed | Expected all tensors to be on the same device, but got mat1 is on cuda:0, different from other tensors on cpu (when checking argument in method wrapper_CUDA_addmm) (see logs/error_BBBP__GINE__PGExplainer__scaffold_20260730_164248.log) |
| BBBP | GINE | PGExplainer | failed | Expected all tensors to be on the same device, but got mat1 is on cuda:0, different from other tensors on cpu (when checking argument in method wrapper_CUDA_addmm) (see logs/error_BBBP__GINE__PGExplainer__random_20260730_164248.log) |
| BACE | GINE | IntegratedGradients | done | acc=0.34 gt_auroc=nan n=100 (capped) [cached] |
| BACE | GINE | IntegratedGradients | done | acc=0.73 gt_auroc=nan n=100 (capped) [cached] |
| BACE | GCN | IntegratedGradients | done | acc=0.85 gt_auroc=nan n=100 (capped) [cached] |
| BACE | GCN | IntegratedGradients | done | acc=0.64 gt_auroc=nan n=100 (capped) [cached] |
| ESOL | GINE | IntegratedGradients | done | rmse=0.929 r2=0.778 n=100 (capped) [cached] |
| ESOL | GINE | IntegratedGradients | done | rmse=0.788 r2=0.869 n=100 (capped) [cached] |
| ESOL | GCN | IntegratedGradients | done | rmse=1.017 r2=0.734 n=100 (capped) [cached] |
| ESOL | GCN | IntegratedGradients | done | rmse=0.951 r2=0.809 n=100 (capped) [cached] |
| ESOL | GAT | IntegratedGradients | done | rmse=0.793 r2=0.838 n=100 (capped) [cached] |
| ESOL | GAT | IntegratedGradients | done | rmse=0.730 r2=0.888 n=100 (capped) [cached] |
| ESOL | GINE | GNNExplainer | done | rmse=0.929 r2=0.778 n=100 (capped) [cached] |
| ESOL | GINE | GNNExplainer | done | rmse=0.788 r2=0.869 n=100 (capped) [cached] |
| FreeSolv | GINE | IntegratedGradients | failed | Expected more than 1 value per channel when training, got input size torch.Size([1, 64]) (see logs/error_FreeSolv__GINE__IntegratedGradients__scaffold_20260730_164248.log) |
| FreeSolv | GINE | IntegratedGradients | done | rmse=1.486 r2=0.803 n=65 (capped) [cached] |
| Lipophilicity | GINE | IntegratedGradients | done | rmse=0.749 r2=0.614 n=100 (capped) [cached] |
| Lipophilicity | GINE | IntegratedGradients | done | rmse=0.737 r2=0.617 n=100 (capped) [cached] |
| ClinTox | GINE | IntegratedGradients | done | acc=0.80 gt_auroc=nan n=100 (capped) [cached] |
| ClinTox | GINE | IntegratedGradients | done | acc=0.71 gt_auroc=nan n=100 (capped) [cached] |
| ClinTox | GINE | GNNExplainer | done | acc=0.80 gt_auroc=nan n=100 (capped) [cached] |
| ClinTox | GINE | GNNExplainer | done | acc=0.71 gt_auroc=nan n=100 (capped) [cached] |
| SIDER | GINE | IntegratedGradients | done | acc=0.57 gt_auroc=nan n=100 (capped) [cached] |
| SIDER | GINE | IntegratedGradients | done | acc=0.71 gt_auroc=nan n=100 (capped) [cached] |
| SIDER | GCN | IntegratedGradients | done | acc=0.65 gt_auroc=nan n=100 (capped) [cached] |
| SIDER | GCN | IntegratedGradients | done | acc=0.64 gt_auroc=nan n=100 (capped) [cached] |
| Tox21 | GINE | IntegratedGradients | done | acc=0.96 gt_auroc=nan n=100 (capped) [cached] |
| Tox21 | GINE | IntegratedGradients | done | acc=0.97 gt_auroc=nan n=100 (capped) [cached] |
| BA-2Motifs | GINE | IntegratedGradients | failed | linear(): argument 'input' (position 1) must be Tensor, not NoneType (see logs/error_BA-2Motifs__GINE__IntegratedGradients__scaffold_20260730_164248.log) |
| BA-2Motifs | GINE | IntegratedGradients | failed | linear(): argument 'input' (position 1) must be Tensor, not NoneType (see logs/error_BA-2Motifs__GINE__IntegratedGradients__random_20260730_164248.log) |
| ShapeGGen | GINE | IntegratedGradients | skipped | ShapeGGen requires GraphXAI which is not installed (No module named 'graphxai'). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | IntegratedGradients | skipped | ShapeGGen requires GraphXAI which is not installed (No module named 'graphxai'). Skipping and logging per Hard Rule 4. |
| DILI | GINE | IntegratedGradients | done | acc=0.69 gt_auroc=nan n=48 (capped) [cached] |
| DILI | GINE | IntegratedGradients | done | acc=0.69 gt_auroc=nan n=48 (capped) [cached] |
| hERG | GINE | IntegratedGradients | done | acc=0.73 gt_auroc=nan n=66 (capped) [cached] |
| hERG | GINE | IntegratedGradients | done | acc=0.80 gt_auroc=nan n=66 (capped) [cached] |

## Blockers

- SynthMotifs__GINE__PGExplainer__scaffold: FAILED Expected all tensors to be on the same device, but got mat1 is on cuda:0, different from other tensors on cpu (when checking argument in method wrapper_CUDA_addmm)
- SynthMotifs__GINE__PGExplainer__random: FAILED Expected all tensors to be on the same device, but got mat1 is on cuda:0, different from other tensors on cpu (when checking argument in method wrapper_CUDA_addmm)
- MUTAG__GINE__IntegratedGradients__scaffold: FAILED can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first.
- MUTAG__GINE__IntegratedGradients__random: FAILED can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first.
- MUTAG__GINE__Saliency__scaffold: FAILED can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first.
- MUTAG__GINE__Saliency__random: FAILED can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first.
- MUTAG__GINE__InputXGradient__scaffold: FAILED can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first.
- MUTAG__GINE__InputXGradient__random: FAILED can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first.
- MUTAG__GINE__GuidedBackprop__scaffold: FAILED can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first.
- MUTAG__GINE__GuidedBackprop__random: FAILED can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first.
- MUTAG__GINE__GNNExplainer__scaffold: FAILED can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first.
- MUTAG__GINE__GNNExplainer__random: FAILED can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first.
- MUTAG__GINE__PGExplainer__scaffold: FAILED Expected all tensors to be on the same device, but got mat1 is on cuda:0, different from other tensors on cpu (when checking argument in method wrapper_CUDA_addmm)
- MUTAG__GINE__PGExplainer__random: FAILED Expected all tensors to be on the same device, but got mat1 is on cuda:0, different from other tensors on cpu (when checking argument in method wrapper_CUDA_addmm)
- MUTAG__GCN__IntegratedGradients__scaffold: FAILED can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first.
- MUTAG__GCN__IntegratedGradients__random: FAILED can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first.
- MUTAG__GAT__IntegratedGradients__scaffold: FAILED can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first.
- MUTAG__GAT__IntegratedGradients__random: FAILED can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first.
- MUTAG__MPNN__IntegratedGradients__scaffold: FAILED can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first.
- MUTAG__MPNN__IntegratedGradients__random: FAILED can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first.
- MUTAG__AttentiveFP__IntegratedGradients__scaffold: FAILED can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first.
- MUTAG__AttentiveFP__IntegratedGradients__random: FAILED can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first.
- BBBP__GINE__PGExplainer__scaffold: FAILED Expected all tensors to be on the same device, but got mat1 is on cuda:0, different from other tensors on cpu (when checking argument in method wrapper_CUDA_addmm)
- BBBP__GINE__PGExplainer__random: FAILED Expected all tensors to be on the same device, but got mat1 is on cuda:0, different from other tensors on cpu (when checking argument in method wrapper_CUDA_addmm)
- FreeSolv__GINE__IntegratedGradients__scaffold: FAILED Expected more than 1 value per channel when training, got input size torch.Size([1, 64])
- BA-2Motifs__GINE__IntegratedGradients__scaffold: FAILED linear(): argument 'input' (position 1) must be Tensor, not NoneType
- BA-2Motifs__GINE__IntegratedGradients__random: FAILED linear(): argument 'input' (position 1) must be Tensor, not NoneType
- ShapeGGen__GINE__IntegratedGradients__scaffold: ShapeGGen requires GraphXAI which is not installed (No module named 'graphxai'). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__IntegratedGradients__random: ShapeGGen requires GraphXAI which is not installed (No module named 'graphxai'). Skipping and logging per Hard Rule 4.
