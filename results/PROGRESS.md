# PROGRESS.md — MolSanity rolling progress

_Last run: `full.yaml` @ 20260731_005714._

## Cell tally

- done: **144**  · failed: **222**  · skipped/blocked: **42**

## Cells (dataset × backbone × attributor)

| dataset | backbone | attributor | status | detail |
| --- | --- | --- | --- | --- |
| SynthMotifs | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__GINE__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| SynthMotifs | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__GINE__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| SynthMotifs | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__GINE__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| SynthMotifs | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__GINE__IntegratedGradients__random__seed0_20260731_005714.log) |
| SynthMotifs | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__GINE__IntegratedGradients__random__seed1_20260731_005714.log) |
| SynthMotifs | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__GINE__IntegratedGradients__random__seed2_20260731_005714.log) |
| SynthMotifs | GINE | Saliency | done | acc=0.90 gt_auroc=0.96492 n=200 (capped) |
| SynthMotifs | GINE | Saliency | done | acc=1.00 gt_auroc=0.98256 n=200 (capped) |
| SynthMotifs | GINE | Saliency | done | acc=0.92 gt_auroc=0.98312 n=200 (capped) |
| SynthMotifs | GINE | Saliency | done | acc=0.98 gt_auroc=0.9934000000000001 n=200 (capped) |
| SynthMotifs | GINE | Saliency | done | acc=0.98 gt_auroc=0.98276 n=200 (capped) |
| SynthMotifs | GINE | Saliency | done | acc=0.94 gt_auroc=0.9599599999999999 n=200 (capped) |
| SynthMotifs | GINE | InputXGradient | done | acc=0.90 gt_auroc=0.95144 n=200 (capped) |
| SynthMotifs | GINE | InputXGradient | done | acc=1.00 gt_auroc=0.9765599999999999 n=200 (capped) |
| SynthMotifs | GINE | InputXGradient | done | acc=0.92 gt_auroc=0.9816000000000001 n=200 (capped) |
| SynthMotifs | GINE | InputXGradient | done | acc=0.98 gt_auroc=0.9872 n=200 (capped) |
| SynthMotifs | GINE | InputXGradient | done | acc=0.98 gt_auroc=0.9632 n=200 (capped) |
| SynthMotifs | GINE | InputXGradient | done | acc=0.94 gt_auroc=0.9592400000000001 n=200 (capped) |
| SynthMotifs | GINE | GuidedBackprop | done | acc=0.90 gt_auroc=0.91328 n=200 (capped) |
| SynthMotifs | GINE | GuidedBackprop | done | acc=1.00 gt_auroc=0.99884 n=200 (capped) |
| SynthMotifs | GINE | GuidedBackprop | done | acc=0.92 gt_auroc=0.98224 n=200 (capped) |
| SynthMotifs | GINE | GuidedBackprop | done | acc=0.98 gt_auroc=0.9992 n=200 (capped) |
| SynthMotifs | GINE | GuidedBackprop | done | acc=0.98 gt_auroc=0.9887999999999999 n=200 (capped) |
| SynthMotifs | GINE | GuidedBackprop | done | acc=0.94 gt_auroc=0.9957600000000001 n=200 (capped) |
| SynthMotifs | GINE | GNNExplainer | done | acc=0.90 gt_auroc=0.6681199999999999 n=200 (capped) |
| SynthMotifs | GINE | GNNExplainer | done | acc=1.00 gt_auroc=0.53792 n=200 (capped) |
| SynthMotifs | GINE | GNNExplainer | done | acc=0.92 gt_auroc=0.7962 n=200 (capped) |
| SynthMotifs | GINE | GNNExplainer | done | acc=0.98 gt_auroc=0.55664 n=200 (capped) |
| SynthMotifs | GINE | GNNExplainer | done | acc=0.98 gt_auroc=0.62324 n=200 (capped) |
| SynthMotifs | GINE | GNNExplainer | done | acc=0.94 gt_auroc=0.6885999999999999 n=200 (capped) |
| SynthMotifs | GINE | PGExplainer | done | acc=0.90 gt_auroc=0.5361 n=200 (capped) |
| SynthMotifs | GINE | PGExplainer | done | acc=1.00 gt_auroc=0.30782 n=200 (capped) |
| SynthMotifs | GINE | PGExplainer | done | acc=0.92 gt_auroc=0.3231 n=200 (capped) |
| SynthMotifs | GINE | PGExplainer | done | acc=0.98 gt_auroc=0.46025999999999995 n=200 (capped) |
| SynthMotifs | GINE | PGExplainer | done | acc=0.98 gt_auroc=0.47098 n=200 (capped) |
| SynthMotifs | GINE | PGExplainer | done | acc=0.94 gt_auroc=0.31392000000000003 n=200 (capped) |
| SynthMotifs | GINE | SubgraphX | failed | cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned (see logs/error_SynthMotifs__GINE__SubgraphX__scaffold__seed0_20260731_005714.log) |
| SynthMotifs | GINE | SubgraphX | failed | cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned (see logs/error_SynthMotifs__GINE__SubgraphX__scaffold__seed1_20260731_005714.log) |
| SynthMotifs | GINE | SubgraphX | failed | cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned (see logs/error_SynthMotifs__GINE__SubgraphX__scaffold__seed2_20260731_005714.log) |
| SynthMotifs | GINE | SubgraphX | failed | cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned (see logs/error_SynthMotifs__GINE__SubgraphX__random__seed0_20260731_005714.log) |
| SynthMotifs | GINE | SubgraphX | failed | cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned (see logs/error_SynthMotifs__GINE__SubgraphX__random__seed1_20260731_005714.log) |
| SynthMotifs | GINE | SubgraphX | failed | cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned (see logs/error_SynthMotifs__GINE__SubgraphX__random__seed2_20260731_005714.log) |
| SynthMotifs | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__GCN__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| SynthMotifs | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__GCN__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| SynthMotifs | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__GCN__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| SynthMotifs | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__GCN__IntegratedGradients__random__seed0_20260731_005714.log) |
| SynthMotifs | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__GCN__IntegratedGradients__random__seed1_20260731_005714.log) |
| SynthMotifs | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__GCN__IntegratedGradients__random__seed2_20260731_005714.log) |
| SynthMotifs | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__GAT__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| SynthMotifs | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__GAT__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| SynthMotifs | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__GAT__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| SynthMotifs | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__GAT__IntegratedGradients__random__seed0_20260731_005714.log) |
| SynthMotifs | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__GAT__IntegratedGradients__random__seed1_20260731_005714.log) |
| SynthMotifs | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__GAT__IntegratedGradients__random__seed2_20260731_005714.log) |
| SynthMotifs | MPNN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__MPNN__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| SynthMotifs | MPNN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__MPNN__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| SynthMotifs | MPNN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__MPNN__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| SynthMotifs | MPNN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__MPNN__IntegratedGradients__random__seed0_20260731_005714.log) |
| SynthMotifs | MPNN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__MPNN__IntegratedGradients__random__seed1_20260731_005714.log) |
| SynthMotifs | MPNN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__MPNN__IntegratedGradients__random__seed2_20260731_005714.log) |
| SynthMotifs | AttentiveFP | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__AttentiveFP__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| SynthMotifs | AttentiveFP | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__AttentiveFP__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| SynthMotifs | AttentiveFP | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__AttentiveFP__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| SynthMotifs | AttentiveFP | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__AttentiveFP__IntegratedGradients__random__seed0_20260731_005714.log) |
| SynthMotifs | AttentiveFP | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__AttentiveFP__IntegratedGradients__random__seed1_20260731_005714.log) |
| SynthMotifs | AttentiveFP | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SynthMotifs__AttentiveFP__IntegratedGradients__random__seed2_20260731_005714.log) |
| MUTAG | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__GINE__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| MUTAG | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__GINE__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| MUTAG | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__GINE__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| MUTAG | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__GINE__IntegratedGradients__random__seed0_20260731_005714.log) |
| MUTAG | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__GINE__IntegratedGradients__random__seed1_20260731_005714.log) |
| MUTAG | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__GINE__IntegratedGradients__random__seed2_20260731_005714.log) |
| MUTAG | GINE | Saliency | done | acc=0.83 gt_auroc=0.009125662843753855 n=53 (capped) |
| MUTAG | GINE | Saliency | done | acc=0.58 gt_auroc=0.10091138565056433 n=53 (capped) |
| MUTAG | GINE | Saliency | done | acc=0.87 gt_auroc=0.013739370343143925 n=53 (capped) |
| MUTAG | GINE | Saliency | done | acc=0.53 gt_auroc=0.029480792196309433 n=58 (capped) |
| MUTAG | GINE | Saliency | done | acc=0.81 gt_auroc=0.005584599740279254 n=58 (capped) |
| MUTAG | GINE | Saliency | done | acc=0.90 gt_auroc=0.0017959770114942526 n=58 (capped) |
| MUTAG | GINE | InputXGradient | done | acc=0.83 gt_auroc=0.032174127512640274 n=53 (capped) |
| MUTAG | GINE | InputXGradient | done | acc=0.58 gt_auroc=0.04944076610280828 n=53 (capped) |
| MUTAG | GINE | InputXGradient | done | acc=0.87 gt_auroc=0.048034317595915824 n=53 (capped) |
| MUTAG | GINE | InputXGradient | done | acc=0.53 gt_auroc=0.06584852774000848 n=58 (capped) |
| MUTAG | GINE | InputXGradient | done | acc=0.81 gt_auroc=0.024886085918833865 n=58 (capped) |
| MUTAG | GINE | InputXGradient | done | acc=0.90 gt_auroc=0.013035591483867345 n=58 (capped) |
| MUTAG | GINE | GuidedBackprop | done | acc=0.83 gt_auroc=0.006614797624786526 n=53 (capped) |
| MUTAG | GINE | GuidedBackprop | done | acc=0.58 gt_auroc=0.014272161122882543 n=53 (capped) |
| MUTAG | GINE | GuidedBackprop | done | acc=0.87 gt_auroc=0.14577408245554746 n=53 (capped) |
| MUTAG | GINE | GuidedBackprop | done | acc=0.53 gt_auroc=0.22485861510962932 n=58 (capped) |
| MUTAG | GINE | GuidedBackprop | done | acc=0.81 gt_auroc=0.030085411861861092 n=58 (capped) |
| MUTAG | GINE | GuidedBackprop | done | acc=0.90 gt_auroc=0.03692739346897562 n=58 (capped) |
| MUTAG | GINE | GNNExplainer | done | acc=0.83 gt_auroc=0.7619577382271612 n=53 (capped) |
| MUTAG | GINE | GNNExplainer | done | acc=0.58 gt_auroc=0.48943992841745343 n=53 (capped) |
| MUTAG | GINE | GNNExplainer | done | acc=0.87 gt_auroc=0.5279947348967882 n=53 (capped) |
| MUTAG | GINE | GNNExplainer | done | acc=0.53 gt_auroc=0.4797479966787776 n=58 (capped) |
| MUTAG | GINE | GNNExplainer | done | acc=0.81 gt_auroc=0.7035586483979112 n=58 (capped) |
| MUTAG | GINE | GNNExplainer | done | acc=0.90 gt_auroc=0.8375396371339576 n=58 (capped) |
| MUTAG | GINE | PGExplainer | done | acc=0.83 gt_auroc=0.039247657324793836 n=53 (capped) |
| MUTAG | GINE | PGExplainer | done | acc=0.58 gt_auroc=0.9881239326300368 n=53 (capped) |
| MUTAG | GINE | PGExplainer | done | acc=0.87 gt_auroc=0.9811567394253298 n=53 (capped) |
| MUTAG | GINE | PGExplainer | done | acc=0.53 gt_auroc=0.9956896551724138 n=58 (capped) |
| MUTAG | GINE | PGExplainer | done | acc=0.81 gt_auroc=0.7430817492176518 n=58 (capped) |
| MUTAG | GINE | PGExplainer | done | acc=0.90 gt_auroc=0.250733136876646 n=58 (capped) |
| MUTAG | GINE | SubgraphX | failed | cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned (see logs/error_MUTAG__GINE__SubgraphX__scaffold__seed0_20260731_005714.log) |
| MUTAG | GINE | SubgraphX | failed | cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned (see logs/error_MUTAG__GINE__SubgraphX__scaffold__seed1_20260731_005714.log) |
| MUTAG | GINE | SubgraphX | failed | cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned (see logs/error_MUTAG__GINE__SubgraphX__scaffold__seed2_20260731_005714.log) |
| MUTAG | GINE | SubgraphX | failed | cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned (see logs/error_MUTAG__GINE__SubgraphX__random__seed0_20260731_005714.log) |
| MUTAG | GINE | SubgraphX | failed | cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned (see logs/error_MUTAG__GINE__SubgraphX__random__seed1_20260731_005714.log) |
| MUTAG | GINE | SubgraphX | failed | cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned (see logs/error_MUTAG__GINE__SubgraphX__random__seed2_20260731_005714.log) |
| MUTAG | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__GCN__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| MUTAG | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__GCN__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| MUTAG | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__GCN__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| MUTAG | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__GCN__IntegratedGradients__random__seed0_20260731_005714.log) |
| MUTAG | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__GCN__IntegratedGradients__random__seed1_20260731_005714.log) |
| MUTAG | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__GCN__IntegratedGradients__random__seed2_20260731_005714.log) |
| MUTAG | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__GAT__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| MUTAG | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__GAT__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| MUTAG | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__GAT__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| MUTAG | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__GAT__IntegratedGradients__random__seed0_20260731_005714.log) |
| MUTAG | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__GAT__IntegratedGradients__random__seed1_20260731_005714.log) |
| MUTAG | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__GAT__IntegratedGradients__random__seed2_20260731_005714.log) |
| MUTAG | MPNN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__MPNN__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| MUTAG | MPNN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__MPNN__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| MUTAG | MPNN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__MPNN__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| MUTAG | MPNN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__MPNN__IntegratedGradients__random__seed0_20260731_005714.log) |
| MUTAG | MPNN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__MPNN__IntegratedGradients__random__seed1_20260731_005714.log) |
| MUTAG | MPNN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__MPNN__IntegratedGradients__random__seed2_20260731_005714.log) |
| MUTAG | AttentiveFP | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__AttentiveFP__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| MUTAG | AttentiveFP | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__AttentiveFP__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| MUTAG | AttentiveFP | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__AttentiveFP__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| MUTAG | AttentiveFP | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__AttentiveFP__IntegratedGradients__random__seed0_20260731_005714.log) |
| MUTAG | AttentiveFP | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__AttentiveFP__IntegratedGradients__random__seed1_20260731_005714.log) |
| MUTAG | AttentiveFP | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MUTAG__AttentiveFP__IntegratedGradients__random__seed2_20260731_005714.log) |
| MolMotif | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__GINE__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| MolMotif | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__GINE__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| MolMotif | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__GINE__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| MolMotif | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__GINE__IntegratedGradients__random__seed0_20260731_005714.log) |
| MolMotif | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__GINE__IntegratedGradients__random__seed1_20260731_005714.log) |
| MolMotif | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__GINE__IntegratedGradients__random__seed2_20260731_005714.log) |
| MolMotif | GINE | Saliency | done | acc=0.98 gt_auroc=0.9989183440977171 n=200 (capped) |
| MolMotif | GINE | Saliency | done | acc=0.98 gt_auroc=0.995255654426607 n=200 (capped) |
| MolMotif | GINE | Saliency | done | acc=0.91 gt_auroc=0.9984666015611943 n=200 (capped) |
| MolMotif | GINE | Saliency | done | acc=0.97 gt_auroc=0.9904156582888339 n=200 (capped) |
| MolMotif | GINE | Saliency | done | acc=0.81 gt_auroc=0.9986173162374535 n=200 (capped) |
| MolMotif | GINE | Saliency | done | acc=1.00 gt_auroc=0.9944049905280087 n=200 (capped) |
| MolMotif | GINE | InputXGradient | done | acc=0.98 gt_auroc=0.9990957912387948 n=200 (capped) |
| MolMotif | GINE | InputXGradient | done | acc=0.98 gt_auroc=0.9959102935845328 n=200 (capped) |
| MolMotif | GINE | InputXGradient | done | acc=0.91 gt_auroc=0.9987395537472417 n=200 (capped) |
| MolMotif | GINE | InputXGradient | done | acc=0.97 gt_auroc=0.9863293047406394 n=200 (capped) |
| MolMotif | GINE | InputXGradient | done | acc=0.81 gt_auroc=0.9996628421900161 n=200 (capped) |
| MolMotif | GINE | InputXGradient | done | acc=1.00 gt_auroc=0.9993121892631697 n=200 (capped) |
| MolMotif | GINE | GuidedBackprop | done | acc=0.98 gt_auroc=0.9935624679649864 n=200 (capped) |
| MolMotif | GINE | GuidedBackprop | done | acc=0.98 gt_auroc=0.9950358288741971 n=200 (capped) |
| MolMotif | GINE | GuidedBackprop | done | acc=0.91 gt_auroc=0.8816589761294222 n=200 (capped) |
| MolMotif | GINE | GuidedBackprop | done | acc=0.97 gt_auroc=0.9814639191095337 n=200 (capped) |
| MolMotif | GINE | GuidedBackprop | done | acc=0.81 gt_auroc=0.9350898441593138 n=200 (capped) |
| MolMotif | GINE | GuidedBackprop | done | acc=1.00 gt_auroc=0.9977738438525415 n=200 (capped) |
| MolMotif | GINE | GNNExplainer | done | acc=0.98 gt_auroc=0.587070376526404 n=200 (capped) |
| MolMotif | GINE | GNNExplainer | done | acc=0.98 gt_auroc=0.5854037192366841 n=200 (capped) |
| MolMotif | GINE | GNNExplainer | done | acc=0.91 gt_auroc=0.6036456576073074 n=200 (capped) |
| MolMotif | GINE | GNNExplainer | done | acc=0.97 gt_auroc=0.6790762316327235 n=200 (capped) |
| MolMotif | GINE | GNNExplainer | done | acc=0.81 gt_auroc=0.6055909663939009 n=200 (capped) |
| MolMotif | GINE | GNNExplainer | done | acc=1.00 gt_auroc=0.6296031121363053 n=200 (capped) |
| MolMotif | GINE | PGExplainer | done | acc=0.98 gt_auroc=0.7156726768377253 n=200 (capped) |
| MolMotif | GINE | PGExplainer | done | acc=0.98 gt_auroc=0.49895402478842005 n=200 (capped) |
| MolMotif | GINE | PGExplainer | done | acc=0.91 gt_auroc=0.24000507740888108 n=200 (capped) |
| MolMotif | GINE | PGExplainer | done | acc=0.97 gt_auroc=0.6491229607774095 n=200 (capped) |
| MolMotif | GINE | PGExplainer | done | acc=0.81 gt_auroc=0.27315924812942816 n=200 (capped) |
| MolMotif | GINE | PGExplainer | done | acc=1.00 gt_auroc=0.584361373075497 n=200 (capped) |
| MolMotif | GINE | SubgraphX | failed | cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned (see logs/error_MolMotif__GINE__SubgraphX__scaffold__seed0_20260731_005714.log) |
| MolMotif | GINE | SubgraphX | failed | cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned (see logs/error_MolMotif__GINE__SubgraphX__scaffold__seed1_20260731_005714.log) |
| MolMotif | GINE | SubgraphX | failed | cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned (see logs/error_MolMotif__GINE__SubgraphX__scaffold__seed2_20260731_005714.log) |
| MolMotif | GINE | SubgraphX | failed | cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned (see logs/error_MolMotif__GINE__SubgraphX__random__seed0_20260731_005714.log) |
| MolMotif | GINE | SubgraphX | failed | cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned (see logs/error_MolMotif__GINE__SubgraphX__random__seed1_20260731_005714.log) |
| MolMotif | GINE | SubgraphX | failed | cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned (see logs/error_MolMotif__GINE__SubgraphX__random__seed2_20260731_005714.log) |
| MolMotif | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__GCN__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| MolMotif | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__GCN__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| MolMotif | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__GCN__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| MolMotif | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__GCN__IntegratedGradients__random__seed0_20260731_005714.log) |
| MolMotif | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__GCN__IntegratedGradients__random__seed1_20260731_005714.log) |
| MolMotif | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__GCN__IntegratedGradients__random__seed2_20260731_005714.log) |
| MolMotif | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__GAT__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| MolMotif | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__GAT__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| MolMotif | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__GAT__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| MolMotif | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__GAT__IntegratedGradients__random__seed0_20260731_005714.log) |
| MolMotif | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__GAT__IntegratedGradients__random__seed1_20260731_005714.log) |
| MolMotif | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__GAT__IntegratedGradients__random__seed2_20260731_005714.log) |
| MolMotif | MPNN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__MPNN__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| MolMotif | MPNN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__MPNN__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| MolMotif | MPNN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__MPNN__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| MolMotif | MPNN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__MPNN__IntegratedGradients__random__seed0_20260731_005714.log) |
| MolMotif | MPNN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__MPNN__IntegratedGradients__random__seed1_20260731_005714.log) |
| MolMotif | MPNN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__MPNN__IntegratedGradients__random__seed2_20260731_005714.log) |
| MolMotif | AttentiveFP | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__AttentiveFP__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| MolMotif | AttentiveFP | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__AttentiveFP__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| MolMotif | AttentiveFP | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__AttentiveFP__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| MolMotif | AttentiveFP | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__AttentiveFP__IntegratedGradients__random__seed0_20260731_005714.log) |
| MolMotif | AttentiveFP | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__AttentiveFP__IntegratedGradients__random__seed1_20260731_005714.log) |
| MolMotif | AttentiveFP | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_MolMotif__AttentiveFP__IntegratedGradients__random__seed2_20260731_005714.log) |
| ShapeGGen | GINE | IntegratedGradients | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | IntegratedGradients | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | IntegratedGradients | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | IntegratedGradients | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | IntegratedGradients | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | IntegratedGradients | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | Saliency | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | Saliency | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | Saliency | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | Saliency | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | Saliency | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | Saliency | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | InputXGradient | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | InputXGradient | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | InputXGradient | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | InputXGradient | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | InputXGradient | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | InputXGradient | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | GuidedBackprop | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | GuidedBackprop | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | GuidedBackprop | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | GuidedBackprop | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | GuidedBackprop | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | GuidedBackprop | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | GNNExplainer | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | GNNExplainer | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | GNNExplainer | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | GNNExplainer | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | GNNExplainer | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | GNNExplainer | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | PGExplainer | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | PGExplainer | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | PGExplainer | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | PGExplainer | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | PGExplainer | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | PGExplainer | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | SubgraphX | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | SubgraphX | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | SubgraphX | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | SubgraphX | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | SubgraphX | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | SubgraphX | skipped | ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4. |
| BBBP | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__GINE__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| BBBP | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__GINE__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| BBBP | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__GINE__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| BBBP | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__GINE__IntegratedGradients__random__seed0_20260731_005714.log) |
| BBBP | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__GINE__IntegratedGradients__random__seed1_20260731_005714.log) |
| BBBP | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__GINE__IntegratedGradients__random__seed2_20260731_005714.log) |
| BBBP | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__GCN__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| BBBP | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__GCN__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| BBBP | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__GCN__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| BBBP | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__GCN__IntegratedGradients__random__seed0_20260731_005714.log) |
| BBBP | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__GCN__IntegratedGradients__random__seed1_20260731_005714.log) |
| BBBP | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__GCN__IntegratedGradients__random__seed2_20260731_005714.log) |
| BBBP | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__GAT__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| BBBP | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__GAT__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| BBBP | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__GAT__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| BBBP | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__GAT__IntegratedGradients__random__seed0_20260731_005714.log) |
| BBBP | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__GAT__IntegratedGradients__random__seed1_20260731_005714.log) |
| BBBP | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__GAT__IntegratedGradients__random__seed2_20260731_005714.log) |
| BBBP | MPNN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__MPNN__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| BBBP | MPNN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__MPNN__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| BBBP | MPNN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__MPNN__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| BBBP | MPNN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__MPNN__IntegratedGradients__random__seed0_20260731_005714.log) |
| BBBP | MPNN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__MPNN__IntegratedGradients__random__seed1_20260731_005714.log) |
| BBBP | MPNN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__MPNN__IntegratedGradients__random__seed2_20260731_005714.log) |
| BBBP | AttentiveFP | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__AttentiveFP__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| BBBP | AttentiveFP | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__AttentiveFP__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| BBBP | AttentiveFP | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__AttentiveFP__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| BBBP | AttentiveFP | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__AttentiveFP__IntegratedGradients__random__seed0_20260731_005714.log) |
| BBBP | AttentiveFP | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__AttentiveFP__IntegratedGradients__random__seed1_20260731_005714.log) |
| BBBP | AttentiveFP | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BBBP__AttentiveFP__IntegratedGradients__random__seed2_20260731_005714.log) |
| BBBP | GINE | GNNExplainer | done | acc=0.92 gt_auroc=nan n=200 (capped) |
| BBBP | GINE | GNNExplainer | done | acc=0.72 gt_auroc=nan n=200 (capped) |
| BBBP | GINE | GNNExplainer | done | acc=0.84 gt_auroc=nan n=200 (capped) |
| BBBP | GINE | GNNExplainer | done | acc=0.74 gt_auroc=nan n=200 (capped) |
| BBBP | GINE | GNNExplainer | done | acc=0.76 gt_auroc=nan n=200 (capped) |
| BBBP | GINE | GNNExplainer | done | acc=0.69 gt_auroc=nan n=200 (capped) |
| BBBP | GINE | PGExplainer | done | acc=0.92 gt_auroc=nan n=200 (capped) |
| BBBP | GINE | PGExplainer | done | acc=0.72 gt_auroc=nan n=200 (capped) |
| BBBP | GINE | PGExplainer | done | acc=0.84 gt_auroc=nan n=200 (capped) |
| BBBP | GINE | PGExplainer | done | acc=0.74 gt_auroc=nan n=200 (capped) |
| BBBP | GINE | PGExplainer | done | acc=0.76 gt_auroc=nan n=200 (capped) |
| BBBP | GINE | PGExplainer | done | acc=0.69 gt_auroc=nan n=200 (capped) |
| BACE | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BACE__GINE__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| BACE | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BACE__GINE__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| BACE | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BACE__GINE__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| BACE | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BACE__GINE__IntegratedGradients__random__seed0_20260731_005714.log) |
| BACE | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BACE__GINE__IntegratedGradients__random__seed1_20260731_005714.log) |
| BACE | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BACE__GINE__IntegratedGradients__random__seed2_20260731_005714.log) |
| BACE | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BACE__GCN__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| BACE | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BACE__GCN__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| BACE | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BACE__GCN__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| BACE | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BACE__GCN__IntegratedGradients__random__seed0_20260731_005714.log) |
| BACE | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BACE__GCN__IntegratedGradients__random__seed1_20260731_005714.log) |
| BACE | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BACE__GCN__IntegratedGradients__random__seed2_20260731_005714.log) |
| ESOL | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_ESOL__GINE__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| ESOL | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_ESOL__GINE__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| ESOL | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_ESOL__GINE__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| ESOL | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_ESOL__GINE__IntegratedGradients__random__seed0_20260731_005714.log) |
| ESOL | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_ESOL__GINE__IntegratedGradients__random__seed1_20260731_005714.log) |
| ESOL | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_ESOL__GINE__IntegratedGradients__random__seed2_20260731_005714.log) |
| ESOL | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_ESOL__GCN__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| ESOL | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_ESOL__GCN__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| ESOL | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_ESOL__GCN__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| ESOL | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_ESOL__GCN__IntegratedGradients__random__seed0_20260731_005714.log) |
| ESOL | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_ESOL__GCN__IntegratedGradients__random__seed1_20260731_005714.log) |
| ESOL | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_ESOL__GCN__IntegratedGradients__random__seed2_20260731_005714.log) |
| ESOL | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_ESOL__GAT__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| ESOL | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_ESOL__GAT__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| ESOL | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_ESOL__GAT__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| ESOL | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_ESOL__GAT__IntegratedGradients__random__seed0_20260731_005714.log) |
| ESOL | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_ESOL__GAT__IntegratedGradients__random__seed1_20260731_005714.log) |
| ESOL | GAT | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_ESOL__GAT__IntegratedGradients__random__seed2_20260731_005714.log) |
| ESOL | GINE | GNNExplainer | done | rmse=0.929 r2=0.778 n=200 (capped) |
| ESOL | GINE | GNNExplainer | done | rmse=0.928 r2=0.812 n=200 (capped) |
| ESOL | GINE | GNNExplainer | done | rmse=0.886 r2=0.829 n=200 (capped) |
| ESOL | GINE | GNNExplainer | done | rmse=0.788 r2=0.869 n=200 (capped) |
| ESOL | GINE | GNNExplainer | done | rmse=0.832 r2=0.825 n=200 (capped) |
| ESOL | GINE | GNNExplainer | done | rmse=0.879 r2=0.833 n=200 (capped) |
| FreeSolv | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_FreeSolv__GINE__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| FreeSolv | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_FreeSolv__GINE__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| FreeSolv | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_FreeSolv__GINE__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| FreeSolv | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_FreeSolv__GINE__IntegratedGradients__random__seed0_20260731_005714.log) |
| FreeSolv | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_FreeSolv__GINE__IntegratedGradients__random__seed1_20260731_005714.log) |
| FreeSolv | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_FreeSolv__GINE__IntegratedGradients__random__seed2_20260731_005714.log) |
| Lipophilicity | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_Lipophilicity__GINE__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| Lipophilicity | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_Lipophilicity__GINE__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| Lipophilicity | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_Lipophilicity__GINE__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| Lipophilicity | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_Lipophilicity__GINE__IntegratedGradients__random__seed0_20260731_005714.log) |
| Lipophilicity | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_Lipophilicity__GINE__IntegratedGradients__random__seed1_20260731_005714.log) |
| Lipophilicity | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_Lipophilicity__GINE__IntegratedGradients__random__seed2_20260731_005714.log) |
| ClinTox | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_ClinTox__GINE__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| ClinTox | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_ClinTox__GINE__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| ClinTox | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_ClinTox__GINE__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| ClinTox | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_ClinTox__GINE__IntegratedGradients__random__seed0_20260731_005714.log) |
| ClinTox | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_ClinTox__GINE__IntegratedGradients__random__seed1_20260731_005714.log) |
| ClinTox | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_ClinTox__GINE__IntegratedGradients__random__seed2_20260731_005714.log) |
| ClinTox | GINE | GNNExplainer | done | acc=0.81 gt_auroc=nan n=200 (capped) |
| ClinTox | GINE | GNNExplainer | done | acc=0.79 gt_auroc=nan n=200 (capped) |
| ClinTox | GINE | GNNExplainer | done | acc=0.66 gt_auroc=nan n=200 (capped) |
| ClinTox | GINE | GNNExplainer | done | acc=0.72 gt_auroc=nan n=200 (capped) |
| ClinTox | GINE | GNNExplainer | done | acc=0.76 gt_auroc=nan n=200 (capped) |
| ClinTox | GINE | GNNExplainer | done | acc=0.70 gt_auroc=nan n=200 (capped) |
| SIDER | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SIDER__GINE__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| SIDER | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SIDER__GINE__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| SIDER | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SIDER__GINE__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| SIDER | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SIDER__GINE__IntegratedGradients__random__seed0_20260731_005714.log) |
| SIDER | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SIDER__GINE__IntegratedGradients__random__seed1_20260731_005714.log) |
| SIDER | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SIDER__GINE__IntegratedGradients__random__seed2_20260731_005714.log) |
| SIDER | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SIDER__GCN__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| SIDER | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SIDER__GCN__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| SIDER | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SIDER__GCN__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| SIDER | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SIDER__GCN__IntegratedGradients__random__seed0_20260731_005714.log) |
| SIDER | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SIDER__GCN__IntegratedGradients__random__seed1_20260731_005714.log) |
| SIDER | GCN | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_SIDER__GCN__IntegratedGradients__random__seed2_20260731_005714.log) |
| Tox21 | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_Tox21__GINE__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| Tox21 | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_Tox21__GINE__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| Tox21 | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_Tox21__GINE__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| Tox21 | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_Tox21__GINE__IntegratedGradients__random__seed0_20260731_005714.log) |
| Tox21 | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_Tox21__GINE__IntegratedGradients__random__seed1_20260731_005714.log) |
| Tox21 | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_Tox21__GINE__IntegratedGradients__random__seed2_20260731_005714.log) |
| BA-2Motifs | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BA-2Motifs__GINE__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| BA-2Motifs | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BA-2Motifs__GINE__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| BA-2Motifs | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BA-2Motifs__GINE__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| BA-2Motifs | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BA-2Motifs__GINE__IntegratedGradients__random__seed0_20260731_005714.log) |
| BA-2Motifs | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BA-2Motifs__GINE__IntegratedGradients__random__seed1_20260731_005714.log) |
| BA-2Motifs | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_BA-2Motifs__GINE__IntegratedGradients__random__seed2_20260731_005714.log) |
| BA-2Motifs | GINE | Saliency | done | acc=0.98 gt_auroc=0.8948 n=200 (capped) |
| BA-2Motifs | GINE | Saliency | done | acc=0.99 gt_auroc=0.9347 n=200 (capped) |
| BA-2Motifs | GINE | Saliency | done | acc=0.90 gt_auroc=0.96335 n=200 (capped) |
| BA-2Motifs | GINE | Saliency | done | acc=0.78 gt_auroc=0.9995 n=200 (capped) |
| BA-2Motifs | GINE | Saliency | done | acc=0.65 gt_auroc=0.9964000000000002 n=200 (capped) |
| BA-2Motifs | GINE | Saliency | done | acc=0.88 gt_auroc=0.92785 n=200 (capped) |
| BA-2Motifs | GINE | InputXGradient | done | acc=0.98 gt_auroc=0.8948 n=200 (capped) |
| BA-2Motifs | GINE | InputXGradient | done | acc=0.99 gt_auroc=0.9347 n=200 (capped) |
| BA-2Motifs | GINE | InputXGradient | done | acc=0.90 gt_auroc=0.96335 n=200 (capped) |
| BA-2Motifs | GINE | InputXGradient | done | acc=0.78 gt_auroc=0.9995 n=200 (capped) |
| BA-2Motifs | GINE | InputXGradient | done | acc=0.65 gt_auroc=0.9964000000000002 n=200 (capped) |
| BA-2Motifs | GINE | InputXGradient | done | acc=0.88 gt_auroc=0.92785 n=200 (capped) |
| BA-2Motifs | GINE | GuidedBackprop | done | acc=0.98 gt_auroc=0.8495999999999999 n=200 (capped) |
| BA-2Motifs | GINE | GuidedBackprop | done | acc=0.99 gt_auroc=0.9341499999999999 n=200 (capped) |
| BA-2Motifs | GINE | GuidedBackprop | done | acc=0.90 gt_auroc=0.9076500000000002 n=200 (capped) |
| BA-2Motifs | GINE | GuidedBackprop | done | acc=0.78 gt_auroc=0.9229 n=200 (capped) |
| BA-2Motifs | GINE | GuidedBackprop | done | acc=0.65 gt_auroc=0.9629000000000001 n=200 (capped) |
| BA-2Motifs | GINE | GuidedBackprop | done | acc=0.88 gt_auroc=0.94825 n=200 (capped) |
| BA-2Motifs | GINE | GNNExplainer | done | acc=0.98 gt_auroc=0.47730000000000006 n=200 (capped) |
| BA-2Motifs | GINE | GNNExplainer | done | acc=0.99 gt_auroc=0.48485 n=200 (capped) |
| BA-2Motifs | GINE | GNNExplainer | done | acc=0.90 gt_auroc=0.5017499999999999 n=200 (capped) |
| BA-2Motifs | GINE | GNNExplainer | done | acc=0.78 gt_auroc=0.5141500000000001 n=200 (capped) |
| BA-2Motifs | GINE | GNNExplainer | done | acc=0.65 gt_auroc=0.45615 n=200 (capped) |
| BA-2Motifs | GINE | GNNExplainer | done | acc=0.88 gt_auroc=0.5716500000000001 n=200 (capped) |
| BA-2Motifs | GINE | PGExplainer | done | acc=0.98 gt_auroc=0.8380500000000001 n=200 (capped) |
| BA-2Motifs | GINE | PGExplainer | done | acc=0.99 gt_auroc=0.857825 n=200 (capped) |
| BA-2Motifs | GINE | PGExplainer | done | acc=0.90 gt_auroc=0.8628750000000001 n=200 (capped) |
| BA-2Motifs | GINE | PGExplainer | done | acc=0.78 gt_auroc=0.37717500000000004 n=200 (capped) |
| BA-2Motifs | GINE | PGExplainer | done | acc=0.65 gt_auroc=0.591275 n=200 (capped) |
| BA-2Motifs | GINE | PGExplainer | done | acc=0.88 gt_auroc=0.10225000000000001 n=200 (capped) |
| DILI | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_DILI__GINE__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| DILI | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_DILI__GINE__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| DILI | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_DILI__GINE__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| DILI | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_DILI__GINE__IntegratedGradients__random__seed0_20260731_005714.log) |
| DILI | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_DILI__GINE__IntegratedGradients__random__seed1_20260731_005714.log) |
| DILI | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_DILI__GINE__IntegratedGradients__random__seed2_20260731_005714.log) |
| hERG | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_hERG__GINE__IntegratedGradients__scaffold__seed0_20260731_005714.log) |
| hERG | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_hERG__GINE__IntegratedGradients__scaffold__seed1_20260731_005714.log) |
| hERG | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_hERG__GINE__IntegratedGradients__scaffold__seed2_20260731_005714.log) |
| hERG | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_hERG__GINE__IntegratedGradients__random__seed0_20260731_005714.log) |
| hERG | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_hERG__GINE__IntegratedGradients__random__seed1_20260731_005714.log) |
| hERG | GINE | IntegratedGradients | failed | index 1 is out of bounds for dimension 0 with size 1 (see logs/error_hERG__GINE__IntegratedGradients__random__seed2_20260731_005714.log) |

## Blockers

- SynthMotifs__GINE__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__GINE__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__GINE__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__GINE__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__GINE__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__GINE__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__GINE__SubgraphX__scaffold__seed0: FAILED cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned
- SynthMotifs__GINE__SubgraphX__scaffold__seed1: FAILED cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned
- SynthMotifs__GINE__SubgraphX__scaffold__seed2: FAILED cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned
- SynthMotifs__GINE__SubgraphX__random__seed0: FAILED cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned
- SynthMotifs__GINE__SubgraphX__random__seed1: FAILED cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned
- SynthMotifs__GINE__SubgraphX__random__seed2: FAILED cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned
- SynthMotifs__GCN__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__GCN__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__GCN__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__GCN__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__GCN__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__GCN__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__GAT__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__GAT__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__GAT__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__GAT__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__GAT__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__GAT__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__MPNN__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__MPNN__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__MPNN__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__MPNN__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__MPNN__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__MPNN__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__AttentiveFP__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__AttentiveFP__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__AttentiveFP__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__AttentiveFP__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__AttentiveFP__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- SynthMotifs__AttentiveFP__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__GINE__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__GINE__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__GINE__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__GINE__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__GINE__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__GINE__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__GINE__SubgraphX__scaffold__seed0: FAILED cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned
- MUTAG__GINE__SubgraphX__scaffold__seed1: FAILED cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned
- MUTAG__GINE__SubgraphX__scaffold__seed2: FAILED cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned
- MUTAG__GINE__SubgraphX__random__seed0: FAILED cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned
- MUTAG__GINE__SubgraphX__random__seed1: FAILED cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned
- MUTAG__GINE__SubgraphX__random__seed2: FAILED cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned
- MUTAG__GCN__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__GCN__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__GCN__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__GCN__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__GCN__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__GCN__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__GAT__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__GAT__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__GAT__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__GAT__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__GAT__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__GAT__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__MPNN__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__MPNN__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__MPNN__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__MPNN__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__MPNN__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__MPNN__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__AttentiveFP__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__AttentiveFP__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__AttentiveFP__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__AttentiveFP__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__AttentiveFP__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- MUTAG__AttentiveFP__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__GINE__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__GINE__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__GINE__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__GINE__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__GINE__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__GINE__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__GINE__SubgraphX__scaffold__seed0: FAILED cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned
- MolMotif__GINE__SubgraphX__scaffold__seed1: FAILED cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned
- MolMotif__GINE__SubgraphX__scaffold__seed2: FAILED cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned
- MolMotif__GINE__SubgraphX__random__seed0: FAILED cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned
- MolMotif__GINE__SubgraphX__random__seed1: FAILED cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned
- MolMotif__GINE__SubgraphX__random__seed2: FAILED cannot pin 'torch.cuda.FloatTensor' only dense CPU tensors can be pinned
- MolMotif__GCN__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__GCN__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__GCN__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__GCN__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__GCN__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__GCN__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__GAT__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__GAT__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__GAT__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__GAT__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__GAT__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__GAT__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__MPNN__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__MPNN__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__MPNN__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__MPNN__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__MPNN__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__MPNN__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__AttentiveFP__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__AttentiveFP__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__AttentiveFP__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__AttentiveFP__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__AttentiveFP__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- MolMotif__AttentiveFP__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- ShapeGGen__GINE__IntegratedGradients__scaffold__seed0: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__IntegratedGradients__scaffold__seed1: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__IntegratedGradients__scaffold__seed2: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__IntegratedGradients__random__seed0: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__IntegratedGradients__random__seed1: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__IntegratedGradients__random__seed2: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__Saliency__scaffold__seed0: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__Saliency__scaffold__seed1: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__Saliency__scaffold__seed2: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__Saliency__random__seed0: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__Saliency__random__seed1: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__Saliency__random__seed2: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__InputXGradient__scaffold__seed0: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__InputXGradient__scaffold__seed1: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__InputXGradient__scaffold__seed2: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__InputXGradient__random__seed0: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__InputXGradient__random__seed1: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__InputXGradient__random__seed2: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__GuidedBackprop__scaffold__seed0: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__GuidedBackprop__scaffold__seed1: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__GuidedBackprop__scaffold__seed2: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__GuidedBackprop__random__seed0: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__GuidedBackprop__random__seed1: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__GuidedBackprop__random__seed2: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__GNNExplainer__scaffold__seed0: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__GNNExplainer__scaffold__seed1: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__GNNExplainer__scaffold__seed2: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__GNNExplainer__random__seed0: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__GNNExplainer__random__seed1: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__GNNExplainer__random__seed2: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__PGExplainer__scaffold__seed0: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__PGExplainer__scaffold__seed1: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__PGExplainer__scaffold__seed2: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__PGExplainer__random__seed0: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__PGExplainer__random__seed1: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__PGExplainer__random__seed2: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__SubgraphX__scaffold__seed0: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__SubgraphX__scaffold__seed1: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__SubgraphX__scaffold__seed2: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__SubgraphX__random__seed0: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__SubgraphX__random__seed1: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__SubgraphX__random__seed2: ShapeGGen requires GraphXAI, which is not importable (No module named 'graphxai'). Install it from a source checkout (its published wheel omits the subpackages). Skipping and logging per Hard Rule 4.
- BBBP__GINE__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__GINE__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__GINE__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__GINE__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__GINE__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__GINE__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__GCN__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__GCN__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__GCN__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__GCN__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__GCN__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__GCN__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__GAT__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__GAT__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__GAT__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__GAT__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__GAT__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__GAT__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__MPNN__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__MPNN__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__MPNN__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__MPNN__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__MPNN__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__MPNN__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__AttentiveFP__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__AttentiveFP__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__AttentiveFP__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__AttentiveFP__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__AttentiveFP__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- BBBP__AttentiveFP__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- BACE__GINE__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- BACE__GINE__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- BACE__GINE__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- BACE__GINE__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- BACE__GINE__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- BACE__GINE__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- BACE__GCN__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- BACE__GCN__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- BACE__GCN__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- BACE__GCN__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- BACE__GCN__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- BACE__GCN__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- ESOL__GINE__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- ESOL__GINE__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- ESOL__GINE__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- ESOL__GINE__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- ESOL__GINE__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- ESOL__GINE__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- ESOL__GCN__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- ESOL__GCN__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- ESOL__GCN__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- ESOL__GCN__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- ESOL__GCN__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- ESOL__GCN__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- ESOL__GAT__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- ESOL__GAT__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- ESOL__GAT__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- ESOL__GAT__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- ESOL__GAT__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- ESOL__GAT__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- FreeSolv__GINE__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- FreeSolv__GINE__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- FreeSolv__GINE__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- FreeSolv__GINE__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- FreeSolv__GINE__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- FreeSolv__GINE__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- Lipophilicity__GINE__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- Lipophilicity__GINE__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- Lipophilicity__GINE__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- Lipophilicity__GINE__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- Lipophilicity__GINE__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- Lipophilicity__GINE__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- ClinTox__GINE__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- ClinTox__GINE__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- ClinTox__GINE__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- ClinTox__GINE__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- ClinTox__GINE__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- ClinTox__GINE__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- SIDER__GINE__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- SIDER__GINE__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- SIDER__GINE__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- SIDER__GINE__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- SIDER__GINE__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- SIDER__GINE__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- SIDER__GCN__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- SIDER__GCN__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- SIDER__GCN__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- SIDER__GCN__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- SIDER__GCN__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- SIDER__GCN__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- Tox21__GINE__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- Tox21__GINE__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- Tox21__GINE__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- Tox21__GINE__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- Tox21__GINE__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- Tox21__GINE__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- BA-2Motifs__GINE__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- BA-2Motifs__GINE__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- BA-2Motifs__GINE__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- BA-2Motifs__GINE__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- BA-2Motifs__GINE__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- BA-2Motifs__GINE__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- DILI__GINE__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- DILI__GINE__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- DILI__GINE__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- DILI__GINE__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- DILI__GINE__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- DILI__GINE__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- hERG__GINE__IntegratedGradients__scaffold__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- hERG__GINE__IntegratedGradients__scaffold__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- hERG__GINE__IntegratedGradients__scaffold__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
- hERG__GINE__IntegratedGradients__random__seed0: FAILED index 1 is out of bounds for dimension 0 with size 1
- hERG__GINE__IntegratedGradients__random__seed1: FAILED index 1 is out of bounds for dimension 0 with size 1
- hERG__GINE__IntegratedGradients__random__seed2: FAILED index 1 is out of bounds for dimension 0 with size 1
