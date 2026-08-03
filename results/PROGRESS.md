# PROGRESS.md — MolSanity rolling progress

_Last run: `full.yaml` @ 20260802_231804._

## Cell tally

- done: **387**  · failed: **21**  · skipped/blocked: **0**

## Cells (dataset × backbone × attributor)

| dataset | backbone | attributor | status | detail |
| --- | --- | --- | --- | --- |
| SynthMotifs | GINE | IntegratedGradients | done | acc=0.90 gt_auroc=0.8886 n=200 (capped) [cached] |
| SynthMotifs | GINE | IntegratedGradients | done | acc=1.00 gt_auroc=0.99248 n=200 (capped) [cached] |
| SynthMotifs | GINE | IntegratedGradients | done | acc=0.92 gt_auroc=0.97808 n=200 (capped) [cached] |
| SynthMotifs | GINE | IntegratedGradients | done | acc=0.98 gt_auroc=0.9968800000000002 n=200 (capped) [cached] |
| SynthMotifs | GINE | IntegratedGradients | done | acc=0.98 gt_auroc=0.99576 n=200 (capped) [cached] |
| SynthMotifs | GINE | IntegratedGradients | done | acc=0.94 gt_auroc=0.97708 n=200 (capped) [cached] |
| SynthMotifs | GINE | Saliency | done | acc=0.90 gt_auroc=0.96492 n=200 (capped) [cached] |
| SynthMotifs | GINE | Saliency | done | acc=1.00 gt_auroc=0.98256 n=200 (capped) [cached] |
| SynthMotifs | GINE | Saliency | done | acc=0.92 gt_auroc=0.98312 n=200 (capped) [cached] |
| SynthMotifs | GINE | Saliency | done | acc=0.98 gt_auroc=0.9934000000000001 n=200 (capped) [cached] |
| SynthMotifs | GINE | Saliency | done | acc=0.98 gt_auroc=0.98276 n=200 (capped) [cached] |
| SynthMotifs | GINE | Saliency | done | acc=0.94 gt_auroc=0.9599599999999999 n=200 (capped) [cached] |
| SynthMotifs | GINE | InputXGradient | done | acc=0.90 gt_auroc=0.95144 n=200 (capped) [cached] |
| SynthMotifs | GINE | InputXGradient | done | acc=1.00 gt_auroc=0.9765599999999999 n=200 (capped) [cached] |
| SynthMotifs | GINE | InputXGradient | done | acc=0.92 gt_auroc=0.9816000000000001 n=200 (capped) [cached] |
| SynthMotifs | GINE | InputXGradient | done | acc=0.98 gt_auroc=0.9872 n=200 (capped) [cached] |
| SynthMotifs | GINE | InputXGradient | done | acc=0.98 gt_auroc=0.9632 n=200 (capped) [cached] |
| SynthMotifs | GINE | InputXGradient | done | acc=0.94 gt_auroc=0.9592400000000001 n=200 (capped) [cached] |
| SynthMotifs | GINE | GuidedBackprop | done | acc=0.90 gt_auroc=0.91328 n=200 (capped) [cached] |
| SynthMotifs | GINE | GuidedBackprop | done | acc=1.00 gt_auroc=0.99884 n=200 (capped) [cached] |
| SynthMotifs | GINE | GuidedBackprop | done | acc=0.92 gt_auroc=0.98224 n=200 (capped) [cached] |
| SynthMotifs | GINE | GuidedBackprop | done | acc=0.98 gt_auroc=0.9992 n=200 (capped) [cached] |
| SynthMotifs | GINE | GuidedBackprop | done | acc=0.98 gt_auroc=0.9887999999999999 n=200 (capped) [cached] |
| SynthMotifs | GINE | GuidedBackprop | done | acc=0.94 gt_auroc=0.9957600000000001 n=200 (capped) [cached] |
| SynthMotifs | GINE | GNNExplainer | done | acc=0.90 gt_auroc=0.67156 n=200 (capped) [cached] |
| SynthMotifs | GINE | GNNExplainer | done | acc=1.00 gt_auroc=0.544 n=200 (capped) [cached] |
| SynthMotifs | GINE | GNNExplainer | done | acc=0.92 gt_auroc=0.79636 n=200 (capped) [cached] |
| SynthMotifs | GINE | GNNExplainer | done | acc=0.98 gt_auroc=0.5642 n=200 (capped) [cached] |
| SynthMotifs | GINE | GNNExplainer | done | acc=0.98 gt_auroc=0.63536 n=200 (capped) [cached] |
| SynthMotifs | GINE | GNNExplainer | done | acc=0.94 gt_auroc=0.6977600000000002 n=200 (capped) [cached] |
| SynthMotifs | GINE | PGExplainer | done | acc=0.90 gt_auroc=0.5361 n=200 (capped) [cached] |
| SynthMotifs | GINE | PGExplainer | done | acc=1.00 gt_auroc=0.30782 n=200 (capped) [cached] |
| SynthMotifs | GINE | PGExplainer | done | acc=0.92 gt_auroc=0.3231 n=200 (capped) [cached] |
| SynthMotifs | GINE | PGExplainer | done | acc=0.98 gt_auroc=0.46025999999999995 n=200 (capped) [cached] |
| SynthMotifs | GINE | PGExplainer | done | acc=0.98 gt_auroc=0.47098 n=200 (capped) [cached] |
| SynthMotifs | GINE | PGExplainer | done | acc=0.94 gt_auroc=0.31392000000000003 n=200 (capped) [cached] |
| SynthMotifs | GINE | SubgraphX | done | acc=0.90 gt_auroc=0.6040000000000001 n=200 (capped) [cached] |
| SynthMotifs | GINE | SubgraphX | done | acc=1.00 gt_auroc=0.8708999999999999 n=200 (capped) [cached] |
| SynthMotifs | GINE | SubgraphX | done | acc=0.92 gt_auroc=0.8409 n=200 (capped) [cached] |
| SynthMotifs | GINE | SubgraphX | done | acc=0.98 gt_auroc=0.6419999999999999 n=200 (capped) [cached] |
| SynthMotifs | GINE | SubgraphX | done | acc=0.98 gt_auroc=0.8237000000000001 n=200 (capped) [cached] |
| SynthMotifs | GINE | SubgraphX | done | acc=0.94 gt_auroc=0.8449999999999999 n=200 (capped) [cached] |
| SynthMotifs | GCN | IntegratedGradients | done | acc=0.64 gt_auroc=0.9875200000000001 n=200 (capped) [cached] |
| SynthMotifs | GCN | IntegratedGradients | done | acc=0.97 gt_auroc=0.9464 n=200 (capped) [cached] |
| SynthMotifs | GCN | IntegratedGradients | done | acc=0.98 gt_auroc=0.9359200000000001 n=200 (capped) [cached] |
| SynthMotifs | GCN | IntegratedGradients | done | acc=0.69 gt_auroc=0.58304 n=200 (capped) [cached] |
| SynthMotifs | GCN | IntegratedGradients | done | acc=0.98 gt_auroc=0.98348 n=200 (capped) [cached] |
| SynthMotifs | GCN | IntegratedGradients | done | acc=0.99 gt_auroc=0.9902799999999999 n=200 (capped) [cached] |
| SynthMotifs | GAT | IntegratedGradients | done | acc=0.95 gt_auroc=0.6007600000000001 n=200 (capped) [cached] |
| SynthMotifs | GAT | IntegratedGradients | done | acc=0.99 gt_auroc=0.9497599999999999 n=200 (capped) [cached] |
| SynthMotifs | GAT | IntegratedGradients | done | acc=0.99 gt_auroc=0.9103999999999999 n=200 (capped) [cached] |
| SynthMotifs | GAT | IntegratedGradients | done | acc=0.99 gt_auroc=0.9200800000000001 n=200 (capped) [cached] |
| SynthMotifs | GAT | IntegratedGradients | done | acc=0.98 gt_auroc=0.8164 n=200 (capped) [cached] |
| SynthMotifs | GAT | IntegratedGradients | done | acc=0.99 gt_auroc=0.64168 n=200 (capped) [cached] |
| SynthMotifs | MPNN | IntegratedGradients | done | acc=0.59 gt_auroc=0.69796 n=200 (capped) [cached] |
| SynthMotifs | MPNN | IntegratedGradients | done | acc=0.86 gt_auroc=0.9218000000000001 n=200 (capped) [cached] |
| SynthMotifs | MPNN | IntegratedGradients | done | acc=0.91 gt_auroc=0.9131200000000002 n=200 (capped) [cached] |
| SynthMotifs | MPNN | IntegratedGradients | done | acc=0.98 gt_auroc=0.81172 n=200 (capped) [cached] |
| SynthMotifs | MPNN | IntegratedGradients | done | acc=0.99 gt_auroc=0.8999600000000001 n=200 (capped) [cached] |
| SynthMotifs | MPNN | IntegratedGradients | done | acc=1.00 gt_auroc=0.9031199999999999 n=200 (capped) [cached] |
| SynthMotifs | AttentiveFP | IntegratedGradients | done | acc=0.91 gt_auroc=0.8753200000000001 n=200 (capped) [cached] |
| SynthMotifs | AttentiveFP | IntegratedGradients | done | acc=0.89 gt_auroc=0.8198400000000001 n=200 (capped) [cached] |
| SynthMotifs | AttentiveFP | IntegratedGradients | done | acc=0.82 gt_auroc=0.9571200000000001 n=200 (capped) [cached] |
| SynthMotifs | AttentiveFP | IntegratedGradients | done | acc=0.97 gt_auroc=0.7764 n=200 (capped) [cached] |
| SynthMotifs | AttentiveFP | IntegratedGradients | done | acc=0.98 gt_auroc=0.9398400000000001 n=200 (capped) [cached] |
| SynthMotifs | AttentiveFP | IntegratedGradients | done | acc=0.98 gt_auroc=0.8982399999999999 n=200 (capped) [cached] |
| MUTAG | GINE | IntegratedGradients | done | acc=0.83 gt_auroc=0.5714079883613735 n=53 (capped) [cached] |
| MUTAG | GINE | IntegratedGradients | done | acc=0.58 gt_auroc=0.016418946080433316 n=53 (capped) [cached] |
| MUTAG | GINE | IntegratedGradients | done | acc=0.87 gt_auroc=0.5276862493982359 n=53 (capped) [cached] |
| MUTAG | GINE | IntegratedGradients | done | acc=0.53 gt_auroc=0.052496601888082625 n=58 (capped) [cached] |
| MUTAG | GINE | IntegratedGradients | done | acc=0.81 gt_auroc=0.6122331818809479 n=58 (capped) [cached] |
| MUTAG | GINE | IntegratedGradients | done | acc=0.90 gt_auroc=0.4956688191982309 n=58 (capped) [cached] |
| MUTAG | GINE | Saliency | done | acc=0.83 gt_auroc=0.009125662843753855 n=53 (capped) [cached] |
| MUTAG | GINE | Saliency | done | acc=0.58 gt_auroc=0.10091138565056433 n=53 (capped) [cached] |
| MUTAG | GINE | Saliency | done | acc=0.87 gt_auroc=0.013739370343143925 n=53 (capped) [cached] |
| MUTAG | GINE | Saliency | done | acc=0.53 gt_auroc=0.029480792196309433 n=58 (capped) [cached] |
| MUTAG | GINE | Saliency | done | acc=0.81 gt_auroc=0.005584599740279254 n=58 (capped) [cached] |
| MUTAG | GINE | Saliency | done | acc=0.90 gt_auroc=0.0017959770114942526 n=58 (capped) [cached] |
| MUTAG | GINE | InputXGradient | done | acc=0.83 gt_auroc=0.032174127512640274 n=53 (capped) [cached] |
| MUTAG | GINE | InputXGradient | done | acc=0.58 gt_auroc=0.04944076610280828 n=53 (capped) [cached] |
| MUTAG | GINE | InputXGradient | done | acc=0.87 gt_auroc=0.048034317595915824 n=53 (capped) [cached] |
| MUTAG | GINE | InputXGradient | done | acc=0.53 gt_auroc=0.06584852774000848 n=58 (capped) [cached] |
| MUTAG | GINE | InputXGradient | done | acc=0.81 gt_auroc=0.024886085918833865 n=58 (capped) [cached] |
| MUTAG | GINE | InputXGradient | done | acc=0.90 gt_auroc=0.013035591483867345 n=58 (capped) [cached] |
| MUTAG | GINE | GuidedBackprop | done | acc=0.83 gt_auroc=0.006614797624786526 n=53 (capped) [cached] |
| MUTAG | GINE | GuidedBackprop | done | acc=0.58 gt_auroc=0.014272161122882543 n=53 (capped) [cached] |
| MUTAG | GINE | GuidedBackprop | done | acc=0.87 gt_auroc=0.14577408245554746 n=53 (capped) [cached] |
| MUTAG | GINE | GuidedBackprop | done | acc=0.53 gt_auroc=0.22485861510962932 n=58 (capped) [cached] |
| MUTAG | GINE | GuidedBackprop | done | acc=0.81 gt_auroc=0.030085411861861092 n=58 (capped) [cached] |
| MUTAG | GINE | GuidedBackprop | done | acc=0.90 gt_auroc=0.03692739346897562 n=58 (capped) [cached] |
| MUTAG | GINE | GNNExplainer | done | acc=0.83 gt_auroc=0.7230835584956007 n=53 (capped) [cached] |
| MUTAG | GINE | GNNExplainer | done | acc=0.58 gt_auroc=0.4818052071659174 n=53 (capped) [cached] |
| MUTAG | GINE | GNNExplainer | done | acc=0.87 gt_auroc=0.5344672202052891 n=53 (capped) [cached] |
| MUTAG | GINE | GNNExplainer | done | acc=0.53 gt_auroc=0.4478129307680524 n=58 (capped) [cached] |
| MUTAG | GINE | GNNExplainer | done | acc=0.81 gt_auroc=0.7279442813882203 n=58 (capped) [cached] |
| MUTAG | GINE | GNNExplainer | done | acc=0.90 gt_auroc=0.8578171940748005 n=58 (capped) [cached] |
| MUTAG | GINE | PGExplainer | done | acc=0.83 gt_auroc=0.039247657324793836 n=53 (capped) [cached] |
| MUTAG | GINE | PGExplainer | done | acc=0.58 gt_auroc=0.9881239326300368 n=53 (capped) [cached] |
| MUTAG | GINE | PGExplainer | done | acc=0.87 gt_auroc=0.9811567394253298 n=53 (capped) [cached] |
| MUTAG | GINE | PGExplainer | done | acc=0.53 gt_auroc=0.9956896551724138 n=58 (capped) [cached] |
| MUTAG | GINE | PGExplainer | done | acc=0.81 gt_auroc=0.7430817492176518 n=58 (capped) [cached] |
| MUTAG | GINE | PGExplainer | done | acc=0.90 gt_auroc=0.250733136876646 n=58 (capped) [cached] |
| MUTAG | GINE | SubgraphX | done | acc=0.83 gt_auroc=0.3503802362084827 n=53 (capped) [cached] |
| MUTAG | GINE | SubgraphX | done | acc=0.58 gt_auroc=0.3525818498002183 n=53 (capped) [cached] |
| MUTAG | GINE | SubgraphX | done | acc=0.87 gt_auroc=0.4524091805653959 n=53 (capped) [cached] |
| MUTAG | GINE | SubgraphX | done | acc=0.53 gt_auroc=0.3419885683957692 n=58 (capped) [cached] |
| MUTAG | GINE | SubgraphX | done | acc=0.81 gt_auroc=0.4886552383286263 n=58 (capped) [cached] |
| MUTAG | GINE | SubgraphX | done | acc=0.90 gt_auroc=0.3478595989878952 n=58 (capped) [cached] |
| MUTAG | GCN | IntegratedGradients | done | acc=0.25 gt_auroc=0.9789477848578848 n=53 (capped) [cached] |
| MUTAG | GCN | IntegratedGradients | done | acc=0.25 gt_auroc=0.033764952521889255 n=53 (capped) [cached] |
| MUTAG | GCN | IntegratedGradients | done | acc=0.75 gt_auroc=0.1742624180193547 n=53 (capped) [cached] |
| MUTAG | GCN | IntegratedGradients | done | acc=0.78 gt_auroc=0.17031666285596303 n=58 (capped) [cached] |
| MUTAG | GCN | IntegratedGradients | done | acc=0.36 gt_auroc=0.37853816411318814 n=58 (capped) [cached] |
| MUTAG | GCN | IntegratedGradients | done | acc=0.78 gt_auroc=0.5507647576486319 n=58 (capped) [cached] |
| MUTAG | GAT | IntegratedGradients | done | acc=0.83 gt_auroc=0.4245492273377955 n=53 (capped) [cached] |
| MUTAG | GAT | IntegratedGradients | done | acc=0.83 gt_auroc=0.3924290193713056 n=53 (capped) [cached] |
| MUTAG | GAT | IntegratedGradients | done | acc=0.75 gt_auroc=0.22234119931123258 n=53 (capped) [cached] |
| MUTAG | GAT | IntegratedGradients | done | acc=0.74 gt_auroc=0.6887873137492813 n=58 (capped) [cached] |
| MUTAG | GAT | IntegratedGradients | done | acc=0.36 gt_auroc=0.049930825345846155 n=58 (capped) [cached] |
| MUTAG | GAT | IntegratedGradients | done | acc=0.76 gt_auroc=0.4611851433162285 n=58 (capped) [cached] |
| MUTAG | MPNN | IntegratedGradients | done | acc=0.83 gt_auroc=0.7057657453328928 n=53 (capped) [cached] |
| MUTAG | MPNN | IntegratedGradients | done | acc=0.25 gt_auroc=0.9512012333044519 n=53 (capped) [cached] |
| MUTAG | MPNN | IntegratedGradients | done | acc=0.83 gt_auroc=0.12351268167028433 n=53 (capped) [cached] |
| MUTAG | MPNN | IntegratedGradients | done | acc=0.86 gt_auroc=0.1440280326690063 n=58 (capped) [cached] |
| MUTAG | MPNN | IntegratedGradients | done | acc=0.72 gt_auroc=0.038234113586080594 n=58 (capped) [cached] |
| MUTAG | MPNN | IntegratedGradients | done | acc=0.78 gt_auroc=0.12661135606749194 n=58 (capped) [cached] |
| MUTAG | AttentiveFP | IntegratedGradients | done | acc=0.72 gt_auroc=0.04384727780954196 n=53 (capped) [cached] |
| MUTAG | AttentiveFP | IntegratedGradients | done | acc=0.75 gt_auroc=0.3373382362283582 n=53 (capped) [cached] |
| MUTAG | AttentiveFP | IntegratedGradients | done | acc=0.75 gt_auroc=0.04433682248610107 n=53 (capped) [cached] |
| MUTAG | AttentiveFP | IntegratedGradients | done | acc=0.72 gt_auroc=0.04713550901431225 n=58 (capped) [cached] |
| MUTAG | AttentiveFP | IntegratedGradients | done | acc=0.81 gt_auroc=0.033601925527034955 n=58 (capped) [cached] |
| MUTAG | AttentiveFP | IntegratedGradients | done | acc=0.67 gt_auroc=0.03910418801392432 n=58 (capped) [cached] |
| MolMotif | GINE | IntegratedGradients | done | acc=0.98 gt_auroc=0.8295341221285595 n=200 (capped) [cached] |
| MolMotif | GINE | IntegratedGradients | done | acc=0.98 gt_auroc=0.8059272792718185 n=200 (capped) [cached] |
| MolMotif | GINE | IntegratedGradients | done | acc=0.91 gt_auroc=0.9839498607263668 n=200 (capped) [cached] |
| MolMotif | GINE | IntegratedGradients | done | acc=0.97 gt_auroc=0.9191083485338464 n=200 (capped) [cached] |
| MolMotif | GINE | IntegratedGradients | done | acc=0.81 gt_auroc=0.9626544605933575 n=200 (capped) [cached] |
| MolMotif | GINE | IntegratedGradients | done | acc=1.00 gt_auroc=0.9724428179553897 n=200 (capped) [cached] |
| MolMotif | GINE | Saliency | done | acc=0.98 gt_auroc=0.9989183440977171 n=200 (capped) [cached] |
| MolMotif | GINE | Saliency | done | acc=0.98 gt_auroc=0.995255654426607 n=200 (capped) [cached] |
| MolMotif | GINE | Saliency | done | acc=0.91 gt_auroc=0.9984666015611943 n=200 (capped) [cached] |
| MolMotif | GINE | Saliency | done | acc=0.97 gt_auroc=0.9904156582888339 n=200 (capped) [cached] |
| MolMotif | GINE | Saliency | done | acc=0.81 gt_auroc=0.9986173162374535 n=200 (capped) [cached] |
| MolMotif | GINE | Saliency | done | acc=1.00 gt_auroc=0.9944049905280087 n=200 (capped) [cached] |
| MolMotif | GINE | InputXGradient | done | acc=0.98 gt_auroc=0.9990957912387948 n=200 (capped) [cached] |
| MolMotif | GINE | InputXGradient | done | acc=0.98 gt_auroc=0.9959102935845328 n=200 (capped) [cached] |
| MolMotif | GINE | InputXGradient | done | acc=0.91 gt_auroc=0.9987395537472417 n=200 (capped) [cached] |
| MolMotif | GINE | InputXGradient | done | acc=0.97 gt_auroc=0.9863293047406394 n=200 (capped) [cached] |
| MolMotif | GINE | InputXGradient | done | acc=0.81 gt_auroc=0.9996628421900161 n=200 (capped) [cached] |
| MolMotif | GINE | InputXGradient | done | acc=1.00 gt_auroc=0.9993121892631697 n=200 (capped) [cached] |
| MolMotif | GINE | GuidedBackprop | done | acc=0.98 gt_auroc=0.9935624679649864 n=200 (capped) [cached] |
| MolMotif | GINE | GuidedBackprop | done | acc=0.98 gt_auroc=0.9950358288741971 n=200 (capped) [cached] |
| MolMotif | GINE | GuidedBackprop | done | acc=0.91 gt_auroc=0.8816589761294222 n=200 (capped) [cached] |
| MolMotif | GINE | GuidedBackprop | done | acc=0.97 gt_auroc=0.9814639191095337 n=200 (capped) [cached] |
| MolMotif | GINE | GuidedBackprop | done | acc=0.81 gt_auroc=0.9350898441593138 n=200 (capped) [cached] |
| MolMotif | GINE | GuidedBackprop | done | acc=1.00 gt_auroc=0.9977738438525415 n=200 (capped) [cached] |
| MolMotif | GINE | GNNExplainer | done | acc=0.98 gt_auroc=0.5908150574125223 n=200 (capped) [cached] |
| MolMotif | GINE | GNNExplainer | done | acc=0.98 gt_auroc=0.5891556326869961 n=200 (capped) [cached] |
| MolMotif | GINE | GNNExplainer | done | acc=0.91 gt_auroc=0.6101405707110381 n=200 (capped) [cached] |
| MolMotif | GINE | GNNExplainer | done | acc=0.97 gt_auroc=0.6833528633217354 n=200 (capped) [cached] |
| MolMotif | GINE | GNNExplainer | done | acc=0.81 gt_auroc=0.6104240422325831 n=200 (capped) [cached] |
| MolMotif | GINE | GNNExplainer | done | acc=1.00 gt_auroc=0.6304748497589063 n=200 (capped) [cached] |
| MolMotif | GINE | PGExplainer | done | acc=0.98 gt_auroc=0.7156726768377253 n=200 (capped) [cached] |
| MolMotif | GINE | PGExplainer | done | acc=0.98 gt_auroc=0.49895402478842005 n=200 (capped) [cached] |
| MolMotif | GINE | PGExplainer | done | acc=0.91 gt_auroc=0.24000507740888108 n=200 (capped) [cached] |
| MolMotif | GINE | PGExplainer | done | acc=0.97 gt_auroc=0.6491229607774095 n=200 (capped) [cached] |
| MolMotif | GINE | PGExplainer | done | acc=0.81 gt_auroc=0.27315924812942816 n=200 (capped) [cached] |
| MolMotif | GINE | PGExplainer | done | acc=1.00 gt_auroc=0.584361373075497 n=200 (capped) [cached] |
| MolMotif | GINE | SubgraphX | done | acc=0.98 gt_auroc=0.474593347727264 n=200 (capped) [cached] |
| MolMotif | GINE | SubgraphX | done | acc=0.98 gt_auroc=0.4895980764369009 n=200 (capped) [cached] |
| MolMotif | GINE | SubgraphX | done | acc=0.91 gt_auroc=0.5125480355506239 n=200 (capped) [cached] |
| MolMotif | GINE | SubgraphX | done | acc=0.97 gt_auroc=0.5727481687608074 n=200 (capped) [cached] |
| MolMotif | GINE | SubgraphX | done | acc=0.81 gt_auroc=0.5347887380679491 n=200 (capped) [cached] |
| MolMotif | GINE | SubgraphX | done | acc=1.00 gt_auroc=0.5557396101480824 n=200 (capped) [cached] |
| MolMotif | GCN | IntegratedGradients | done | acc=0.98 gt_auroc=0.9583683262576951 n=200 (capped) [cached] |
| MolMotif | GCN | IntegratedGradients | done | acc=0.96 gt_auroc=0.9653365421374366 n=200 (capped) [cached] |
| MolMotif | GCN | IntegratedGradients | done | acc=0.95 gt_auroc=0.8925166806268993 n=200 (capped) [cached] |
| MolMotif | GCN | IntegratedGradients | done | acc=0.97 gt_auroc=0.9977217535815818 n=200 (capped) [cached] |
| MolMotif | GCN | IntegratedGradients | done | acc=0.68 gt_auroc=0.9821226072322425 n=200 (capped) [cached] |
| MolMotif | GCN | IntegratedGradients | done | acc=0.96 gt_auroc=0.8495070580514895 n=200 (capped) [cached] |
| MolMotif | GAT | IntegratedGradients | done | acc=0.96 gt_auroc=0.6786317874060145 n=200 (capped) [cached] |
| MolMotif | GAT | IntegratedGradients | done | acc=0.97 gt_auroc=0.9457644242032968 n=200 (capped) [cached] |
| MolMotif | GAT | IntegratedGradients | done | acc=0.99 gt_auroc=0.873009127265564 n=200 (capped) [cached] |
| MolMotif | GAT | IntegratedGradients | done | acc=1.00 gt_auroc=0.7960669305032867 n=200 (capped) [cached] |
| MolMotif | GAT | IntegratedGradients | done | acc=1.00 gt_auroc=0.9957610663283009 n=200 (capped) [cached] |
| MolMotif | GAT | IntegratedGradients | done | acc=1.00 gt_auroc=0.7331860475743693 n=200 (capped) [cached] |
| MolMotif | MPNN | IntegratedGradients | done | acc=0.97 gt_auroc=0.7715475744966365 n=200 (capped) [cached] |
| MolMotif | MPNN | IntegratedGradients | done | acc=0.97 gt_auroc=0.7927840896268697 n=200 (capped) [cached] |
| MolMotif | MPNN | IntegratedGradients | done | acc=0.98 gt_auroc=0.9395307660859127 n=200 (capped) [cached] |
| MolMotif | MPNN | IntegratedGradients | done | acc=1.00 gt_auroc=0.7825333316487607 n=200 (capped) [cached] |
| MolMotif | MPNN | IntegratedGradients | done | acc=1.00 gt_auroc=0.8737012355533246 n=200 (capped) [cached] |
| MolMotif | MPNN | IntegratedGradients | done | acc=1.00 gt_auroc=0.9617536793811429 n=200 (capped) [cached] |
| MolMotif | AttentiveFP | IntegratedGradients | done | acc=0.99 gt_auroc=0.9802314229804233 n=200 (capped) [cached] |
| MolMotif | AttentiveFP | IntegratedGradients | done | acc=0.99 gt_auroc=0.9248431084725615 n=200 (capped) [cached] |
| MolMotif | AttentiveFP | IntegratedGradients | done | acc=0.99 gt_auroc=0.995412136250156 n=200 (capped) [cached] |
| MolMotif | AttentiveFP | IntegratedGradients | done | acc=0.98 gt_auroc=0.9868429032353114 n=200 (capped) [cached] |
| MolMotif | AttentiveFP | IntegratedGradients | done | acc=0.91 gt_auroc=0.9279166281920552 n=200 (capped) [cached] |
| MolMotif | AttentiveFP | IntegratedGradients | done | acc=0.97 gt_auroc=0.9862300114597343 n=200 (capped) [cached] |
| ShapeGGen | GINE | IntegratedGradients | failed | list index out of range (see logs/error_ShapeGGen__GINE__IntegratedGradients__scaffold__seed0_20260802_231804.log) |
| ShapeGGen | GINE | IntegratedGradients | failed | list index out of range (see logs/error_ShapeGGen__GINE__IntegratedGradients__scaffold__seed1_20260802_231804.log) |
| ShapeGGen | GINE | IntegratedGradients | failed | list index out of range (see logs/error_ShapeGGen__GINE__IntegratedGradients__scaffold__seed2_20260802_231804.log) |
| ShapeGGen | GINE | IntegratedGradients | done | acc=0.74 gt_auroc=0.7316025759073379 n=50 (capped) [cached] |
| ShapeGGen | GINE | IntegratedGradients | done | acc=0.82 gt_auroc=0.7162817404674897 n=50 (capped) [cached] |
| ShapeGGen | GINE | IntegratedGradients | done | acc=0.78 gt_auroc=0.751419329700282 n=50 (capped) [cached] |
| ShapeGGen | GINE | Saliency | failed | list index out of range (see logs/error_ShapeGGen__GINE__Saliency__scaffold__seed0_20260802_231804.log) |
| ShapeGGen | GINE | Saliency | failed | list index out of range (see logs/error_ShapeGGen__GINE__Saliency__scaffold__seed1_20260802_231804.log) |
| ShapeGGen | GINE | Saliency | failed | list index out of range (see logs/error_ShapeGGen__GINE__Saliency__scaffold__seed2_20260802_231804.log) |
| ShapeGGen | GINE | Saliency | done | acc=0.74 gt_auroc=0.7617182034676082 n=50 (capped) [cached] |
| ShapeGGen | GINE | Saliency | done | acc=0.82 gt_auroc=0.7762731758852207 n=50 (capped) [cached] |
| ShapeGGen | GINE | Saliency | done | acc=0.78 gt_auroc=0.769384145550217 n=50 (capped) [cached] |
| ShapeGGen | GINE | InputXGradient | failed | list index out of range (see logs/error_ShapeGGen__GINE__InputXGradient__scaffold__seed0_20260802_231804.log) |
| ShapeGGen | GINE | InputXGradient | failed | list index out of range (see logs/error_ShapeGGen__GINE__InputXGradient__scaffold__seed1_20260802_231804.log) |
| ShapeGGen | GINE | InputXGradient | failed | list index out of range (see logs/error_ShapeGGen__GINE__InputXGradient__scaffold__seed2_20260802_231804.log) |
| ShapeGGen | GINE | InputXGradient | done | acc=0.74 gt_auroc=0.7240912044304902 n=50 (capped) [cached] |
| ShapeGGen | GINE | InputXGradient | done | acc=0.82 gt_auroc=0.7180203965359777 n=50 (capped) [cached] |
| ShapeGGen | GINE | InputXGradient | done | acc=0.78 gt_auroc=0.7320569259003783 n=50 (capped) [cached] |
| ShapeGGen | GINE | GuidedBackprop | failed | list index out of range (see logs/error_ShapeGGen__GINE__GuidedBackprop__scaffold__seed0_20260802_231804.log) |
| ShapeGGen | GINE | GuidedBackprop | failed | list index out of range (see logs/error_ShapeGGen__GINE__GuidedBackprop__scaffold__seed1_20260802_231804.log) |
| ShapeGGen | GINE | GuidedBackprop | failed | list index out of range (see logs/error_ShapeGGen__GINE__GuidedBackprop__scaffold__seed2_20260802_231804.log) |
| ShapeGGen | GINE | GuidedBackprop | done | acc=0.74 gt_auroc=0.7540469705558992 n=50 (capped) [cached] |
| ShapeGGen | GINE | GuidedBackprop | done | acc=0.82 gt_auroc=0.7752071797056042 n=50 (capped) [cached] |
| ShapeGGen | GINE | GuidedBackprop | done | acc=0.78 gt_auroc=0.7909234349865302 n=50 (capped) [cached] |
| ShapeGGen | GINE | GNNExplainer | failed | list index out of range (see logs/error_ShapeGGen__GINE__GNNExplainer__scaffold__seed0_20260802_231804.log) |
| ShapeGGen | GINE | GNNExplainer | failed | list index out of range (see logs/error_ShapeGGen__GINE__GNNExplainer__scaffold__seed1_20260802_231804.log) |
| ShapeGGen | GINE | GNNExplainer | failed | list index out of range (see logs/error_ShapeGGen__GINE__GNNExplainer__scaffold__seed2_20260802_231804.log) |
| ShapeGGen | GINE | GNNExplainer | done | acc=0.74 gt_auroc=0.5549694652789892 n=50 (capped) [cached] |
| ShapeGGen | GINE | GNNExplainer | done | acc=0.82 gt_auroc=0.6098561532033171 n=50 (capped) [cached] |
| ShapeGGen | GINE | GNNExplainer | done | acc=0.78 gt_auroc=0.4831129766838101 n=50 (capped) [cached] |
| ShapeGGen | GINE | PGExplainer | failed | list index out of range (see logs/error_ShapeGGen__GINE__PGExplainer__scaffold__seed0_20260802_231804.log) |
| ShapeGGen | GINE | PGExplainer | failed | list index out of range (see logs/error_ShapeGGen__GINE__PGExplainer__scaffold__seed1_20260802_231804.log) |
| ShapeGGen | GINE | PGExplainer | failed | list index out of range (see logs/error_ShapeGGen__GINE__PGExplainer__scaffold__seed2_20260802_231804.log) |
| ShapeGGen | GINE | PGExplainer | done | acc=0.74 gt_auroc=0.5030558353683354 n=50 (capped) [cached] |
| ShapeGGen | GINE | PGExplainer | done | acc=0.82 gt_auroc=0.5058584091173377 n=50 (capped) [cached] |
| ShapeGGen | GINE | PGExplainer | done | acc=0.78 gt_auroc=0.4889872839792483 n=50 (capped) [cached] |
| ShapeGGen | GINE | SubgraphX | failed | list index out of range (see logs/error_ShapeGGen__GINE__SubgraphX__scaffold__seed0_20260802_231804.log) |
| ShapeGGen | GINE | SubgraphX | failed | list index out of range (see logs/error_ShapeGGen__GINE__SubgraphX__scaffold__seed1_20260802_231804.log) |
| ShapeGGen | GINE | SubgraphX | failed | list index out of range (see logs/error_ShapeGGen__GINE__SubgraphX__scaffold__seed2_20260802_231804.log) |
| ShapeGGen | GINE | SubgraphX | done | acc=0.74 gt_auroc=0.6757917637917638 n=50 (capped) [cached] |
| ShapeGGen | GINE | SubgraphX | done | acc=0.82 gt_auroc=0.6366717383923266 n=50 (capped) [cached] |
| ShapeGGen | GINE | SubgraphX | done | acc=0.78 gt_auroc=0.6197210289710289 n=50 (capped) [cached] |
| BBBP | GINE | IntegratedGradients | done | acc=0.92 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GINE | IntegratedGradients | done | acc=0.72 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GINE | IntegratedGradients | done | acc=0.84 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GINE | IntegratedGradients | done | acc=0.74 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GINE | IntegratedGradients | done | acc=0.76 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GINE | IntegratedGradients | done | acc=0.69 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GCN | IntegratedGradients | done | acc=0.98 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GCN | IntegratedGradients | done | acc=0.92 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GCN | IntegratedGradients | done | acc=0.97 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GCN | IntegratedGradients | done | acc=0.73 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GCN | IntegratedGradients | done | acc=0.71 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GCN | IntegratedGradients | done | acc=0.78 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GAT | IntegratedGradients | done | acc=0.99 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GAT | IntegratedGradients | done | acc=0.89 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GAT | IntegratedGradients | done | acc=0.97 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GAT | IntegratedGradients | done | acc=0.73 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GAT | IntegratedGradients | done | acc=0.74 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GAT | IntegratedGradients | done | acc=0.73 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | MPNN | IntegratedGradients | done | acc=0.87 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | MPNN | IntegratedGradients | done | acc=0.01 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | MPNN | IntegratedGradients | done | acc=0.95 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | MPNN | IntegratedGradients | done | acc=0.74 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | MPNN | IntegratedGradients | done | acc=0.78 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | MPNN | IntegratedGradients | done | acc=0.76 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | AttentiveFP | IntegratedGradients | done | acc=0.94 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | AttentiveFP | IntegratedGradients | done | acc=0.90 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | AttentiveFP | IntegratedGradients | done | acc=0.94 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | AttentiveFP | IntegratedGradients | done | acc=0.79 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | AttentiveFP | IntegratedGradients | done | acc=0.74 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | AttentiveFP | IntegratedGradients | done | acc=0.74 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GINE | GNNExplainer | done | acc=0.92 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GINE | GNNExplainer | done | acc=0.72 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GINE | GNNExplainer | done | acc=0.84 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GINE | GNNExplainer | done | acc=0.74 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GINE | GNNExplainer | done | acc=0.76 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GINE | GNNExplainer | done | acc=0.69 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GINE | PGExplainer | done | acc=0.92 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GINE | PGExplainer | done | acc=0.72 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GINE | PGExplainer | done | acc=0.84 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GINE | PGExplainer | done | acc=0.74 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GINE | PGExplainer | done | acc=0.76 gt_auroc=nan n=200 (capped) [cached] |
| BBBP | GINE | PGExplainer | done | acc=0.69 gt_auroc=nan n=200 (capped) [cached] |
| BACE | GINE | IntegratedGradients | done | acc=0.47 gt_auroc=nan n=200 (capped) [cached] |
| BACE | GINE | IntegratedGradients | done | acc=0.77 gt_auroc=nan n=200 (capped) [cached] |
| BACE | GINE | IntegratedGradients | done | acc=0.01 gt_auroc=nan n=200 (capped) [cached] |
| BACE | GINE | IntegratedGradients | done | acc=0.81 gt_auroc=nan n=200 (capped) [cached] |
| BACE | GINE | IntegratedGradients | done | acc=0.69 gt_auroc=nan n=200 (capped) [cached] |
| BACE | GINE | IntegratedGradients | done | acc=0.69 gt_auroc=nan n=200 (capped) [cached] |
| BACE | GCN | IntegratedGradients | done | acc=0.83 gt_auroc=nan n=200 (capped) [cached] |
| BACE | GCN | IntegratedGradients | done | acc=0.58 gt_auroc=nan n=200 (capped) [cached] |
| BACE | GCN | IntegratedGradients | done | acc=0.85 gt_auroc=nan n=200 (capped) [cached] |
| BACE | GCN | IntegratedGradients | done | acc=0.72 gt_auroc=nan n=200 (capped) [cached] |
| BACE | GCN | IntegratedGradients | done | acc=0.58 gt_auroc=nan n=200 (capped) [cached] |
| BACE | GCN | IntegratedGradients | done | acc=0.85 gt_auroc=nan n=200 (capped) [cached] |
| ESOL | GINE | IntegratedGradients | done | rmse=0.929 r2=0.778 n=200 (capped) [cached] |
| ESOL | GINE | IntegratedGradients | done | rmse=0.928 r2=0.812 n=200 (capped) [cached] |
| ESOL | GINE | IntegratedGradients | done | rmse=0.886 r2=0.829 n=200 (capped) [cached] |
| ESOL | GINE | IntegratedGradients | done | rmse=0.788 r2=0.869 n=200 (capped) [cached] |
| ESOL | GINE | IntegratedGradients | done | rmse=0.832 r2=0.825 n=200 (capped) [cached] |
| ESOL | GINE | IntegratedGradients | done | rmse=0.879 r2=0.833 n=200 (capped) [cached] |
| ESOL | GCN | IntegratedGradients | done | rmse=1.017 r2=0.734 n=200 (capped) [cached] |
| ESOL | GCN | IntegratedGradients | done | rmse=1.062 r2=0.755 n=200 (capped) [cached] |
| ESOL | GCN | IntegratedGradients | done | rmse=0.972 r2=0.794 n=200 (capped) [cached] |
| ESOL | GCN | IntegratedGradients | done | rmse=0.951 r2=0.809 n=200 (capped) [cached] |
| ESOL | GCN | IntegratedGradients | done | rmse=0.929 r2=0.782 n=200 (capped) [cached] |
| ESOL | GCN | IntegratedGradients | done | rmse=0.961 r2=0.800 n=200 (capped) [cached] |
| ESOL | GAT | IntegratedGradients | done | rmse=0.793 r2=0.838 n=200 (capped) [cached] |
| ESOL | GAT | IntegratedGradients | done | rmse=0.829 r2=0.850 n=200 (capped) [cached] |
| ESOL | GAT | IntegratedGradients | done | rmse=0.894 r2=0.826 n=200 (capped) [cached] |
| ESOL | GAT | IntegratedGradients | done | rmse=0.730 r2=0.888 n=200 (capped) [cached] |
| ESOL | GAT | IntegratedGradients | done | rmse=0.810 r2=0.834 n=200 (capped) [cached] |
| ESOL | GAT | IntegratedGradients | done | rmse=0.751 r2=0.878 n=200 (capped) [cached] |
| ESOL | GINE | GNNExplainer | done | rmse=0.929 r2=0.778 n=200 (capped) [cached] |
| ESOL | GINE | GNNExplainer | done | rmse=0.928 r2=0.812 n=200 (capped) [cached] |
| ESOL | GINE | GNNExplainer | done | rmse=0.886 r2=0.829 n=200 (capped) [cached] |
| ESOL | GINE | GNNExplainer | done | rmse=0.788 r2=0.869 n=200 (capped) [cached] |
| ESOL | GINE | GNNExplainer | done | rmse=0.832 r2=0.825 n=200 (capped) [cached] |
| ESOL | GINE | GNNExplainer | done | rmse=0.879 r2=0.833 n=200 (capped) [cached] |
| FreeSolv | GINE | IntegratedGradients | done | rmse=1.304 r2=0.881 n=193 (capped) [cached] |
| FreeSolv | GINE | IntegratedGradients | done | rmse=1.425 r2=0.847 n=193 (capped) [cached] |
| FreeSolv | GINE | IntegratedGradients | done | rmse=1.529 r2=0.824 n=193 (capped) [cached] |
| FreeSolv | GINE | IntegratedGradients | done | rmse=1.486 r2=0.803 n=193 (capped) [cached] |
| FreeSolv | GINE | IntegratedGradients | done | rmse=1.346 r2=0.857 n=193 (capped) [cached] |
| FreeSolv | GINE | IntegratedGradients | done | rmse=1.618 r2=0.830 n=193 (capped) [cached] |
| Lipophilicity | GINE | IntegratedGradients | done | rmse=0.749 r2=0.614 n=200 (capped) [cached] |
| Lipophilicity | GINE | IntegratedGradients | done | rmse=0.764 r2=0.599 n=200 (capped) [cached] |
| Lipophilicity | GINE | IntegratedGradients | done | rmse=0.754 r2=0.609 n=200 (capped) [cached] |
| Lipophilicity | GINE | IntegratedGradients | done | rmse=0.737 r2=0.617 n=200 (capped) [cached] |
| Lipophilicity | GINE | IntegratedGradients | done | rmse=0.798 r2=0.527 n=200 (capped) [cached] |
| Lipophilicity | GINE | IntegratedGradients | done | rmse=0.783 r2=0.563 n=200 (capped) [cached] |
| ClinTox | GINE | IntegratedGradients | done | acc=0.81 gt_auroc=nan n=200 (capped) [cached] |
| ClinTox | GINE | IntegratedGradients | done | acc=0.79 gt_auroc=nan n=200 (capped) [cached] |
| ClinTox | GINE | IntegratedGradients | done | acc=0.66 gt_auroc=nan n=200 (capped) [cached] |
| ClinTox | GINE | IntegratedGradients | done | acc=0.72 gt_auroc=nan n=200 (capped) [cached] |
| ClinTox | GINE | IntegratedGradients | done | acc=0.76 gt_auroc=nan n=200 (capped) [cached] |
| ClinTox | GINE | IntegratedGradients | done | acc=0.70 gt_auroc=nan n=200 (capped) [cached] |
| ClinTox | GINE | GNNExplainer | done | acc=0.81 gt_auroc=nan n=200 (capped) [cached] |
| ClinTox | GINE | GNNExplainer | done | acc=0.79 gt_auroc=nan n=200 (capped) |
| ClinTox | GINE | GNNExplainer | done | acc=0.66 gt_auroc=nan n=200 (capped) |
| ClinTox | GINE | GNNExplainer | done | acc=0.72 gt_auroc=nan n=200 (capped) |
| ClinTox | GINE | GNNExplainer | done | acc=0.76 gt_auroc=nan n=200 (capped) |
| ClinTox | GINE | GNNExplainer | done | acc=0.70 gt_auroc=nan n=200 (capped) |
| SIDER | GINE | IntegratedGradients | done | acc=0.60 gt_auroc=nan n=200 (capped) |
| SIDER | GINE | IntegratedGradients | done | acc=0.62 gt_auroc=nan n=200 (capped) |
| SIDER | GINE | IntegratedGradients | done | acc=0.58 gt_auroc=nan n=200 (capped) |
| SIDER | GINE | IntegratedGradients | done | acc=0.67 gt_auroc=nan n=200 (capped) |
| SIDER | GINE | IntegratedGradients | done | acc=0.61 gt_auroc=nan n=200 (capped) |
| SIDER | GINE | IntegratedGradients | done | acc=0.65 gt_auroc=nan n=200 (capped) |
| SIDER | GCN | IntegratedGradients | done | acc=0.60 gt_auroc=nan n=200 (capped) |
| SIDER | GCN | IntegratedGradients | done | acc=0.65 gt_auroc=nan n=200 (capped) |
| SIDER | GCN | IntegratedGradients | done | acc=0.57 gt_auroc=nan n=200 (capped) |
| SIDER | GCN | IntegratedGradients | done | acc=0.68 gt_auroc=nan n=200 (capped) |
| SIDER | GCN | IntegratedGradients | done | acc=0.62 gt_auroc=nan n=200 (capped) |
| SIDER | GCN | IntegratedGradients | done | acc=0.63 gt_auroc=nan n=200 (capped) |
| Tox21 | GINE | IntegratedGradients | done | acc=0.97 gt_auroc=nan n=200 (capped) |
| Tox21 | GINE | IntegratedGradients | done | acc=0.95 gt_auroc=nan n=200 (capped) |
| Tox21 | GINE | IntegratedGradients | done | acc=0.64 gt_auroc=nan n=200 (capped) |
| Tox21 | GINE | IntegratedGradients | done | acc=0.94 gt_auroc=nan n=200 (capped) |
| Tox21 | GINE | IntegratedGradients | done | acc=0.95 gt_auroc=nan n=200 (capped) |
| Tox21 | GINE | IntegratedGradients | done | acc=0.93 gt_auroc=nan n=200 (capped) |
| BA-2Motifs | GINE | IntegratedGradients | done | acc=0.98 gt_auroc=0.8615 n=200 (capped) |
| BA-2Motifs | GINE | IntegratedGradients | done | acc=0.99 gt_auroc=0.8916000000000001 n=200 (capped) |
| BA-2Motifs | GINE | IntegratedGradients | done | acc=0.90 gt_auroc=0.9468000000000001 n=200 (capped) |
| BA-2Motifs | GINE | IntegratedGradients | done | acc=0.78 gt_auroc=0.9962000000000001 n=200 (capped) |
| BA-2Motifs | GINE | IntegratedGradients | done | acc=0.65 gt_auroc=1.0 n=200 (capped) |
| BA-2Motifs | GINE | IntegratedGradients | done | acc=0.88 gt_auroc=0.9940000000000001 n=200 (capped) |
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
| BA-2Motifs | GINE | GNNExplainer | done | acc=0.98 gt_auroc=0.48475000000000007 n=200 (capped) |
| BA-2Motifs | GINE | GNNExplainer | done | acc=0.99 gt_auroc=0.49970000000000003 n=200 (capped) |
| BA-2Motifs | GINE | GNNExplainer | done | acc=0.90 gt_auroc=0.5034000000000001 n=200 (capped) |
| BA-2Motifs | GINE | GNNExplainer | done | acc=0.78 gt_auroc=0.50115 n=200 (capped) |
| BA-2Motifs | GINE | GNNExplainer | done | acc=0.65 gt_auroc=0.4585 n=200 (capped) |
| BA-2Motifs | GINE | GNNExplainer | done | acc=0.88 gt_auroc=0.5737000000000001 n=200 (capped) |
| BA-2Motifs | GINE | PGExplainer | done | acc=0.98 gt_auroc=0.9538499999999999 n=200 (capped) |
| BA-2Motifs | GINE | PGExplainer | done | acc=0.99 gt_auroc=0.8572749999999999 n=200 (capped) |
| BA-2Motifs | GINE | PGExplainer | done | acc=0.90 gt_auroc=0.8807250000000001 n=200 (capped) |
| BA-2Motifs | GINE | PGExplainer | done | acc=0.78 gt_auroc=0.4854 n=200 (capped) |
| BA-2Motifs | GINE | PGExplainer | done | acc=0.65 gt_auroc=0.6038000000000001 n=200 (capped) |
| BA-2Motifs | GINE | PGExplainer | done | acc=0.88 gt_auroc=0.10402499999999999 n=200 (capped) |
| DILI | GINE | IntegratedGradients | done | acc=0.77 gt_auroc=nan n=142 (capped) |
| DILI | GINE | IntegratedGradients | done | acc=0.78 gt_auroc=nan n=142 (capped) |
| DILI | GINE | IntegratedGradients | done | acc=0.71 gt_auroc=nan n=142 (capped) |
| DILI | GINE | IntegratedGradients | done | acc=0.82 gt_auroc=nan n=142 (capped) |
| DILI | GINE | IntegratedGradients | done | acc=0.61 gt_auroc=nan n=142 (capped) |
| DILI | GINE | IntegratedGradients | done | acc=0.70 gt_auroc=nan n=142 (capped) |
| hERG | GINE | IntegratedGradients | done | acc=0.69 gt_auroc=nan n=197 (capped) |
| hERG | GINE | IntegratedGradients | done | acc=0.20 gt_auroc=nan n=197 (capped) |
| hERG | GINE | IntegratedGradients | done | acc=0.20 gt_auroc=nan n=197 (capped) |
| hERG | GINE | IntegratedGradients | done | acc=0.79 gt_auroc=nan n=197 (capped) |
| hERG | GINE | IntegratedGradients | done | acc=0.43 gt_auroc=nan n=197 (capped) |
| hERG | GINE | IntegratedGradients | done | acc=0.74 gt_auroc=nan n=197 (capped) |

## Blockers

- ShapeGGen__GINE__IntegratedGradients__scaffold__seed0: FAILED list index out of range
- ShapeGGen__GINE__IntegratedGradients__scaffold__seed1: FAILED list index out of range
- ShapeGGen__GINE__IntegratedGradients__scaffold__seed2: FAILED list index out of range
- ShapeGGen__GINE__Saliency__scaffold__seed0: FAILED list index out of range
- ShapeGGen__GINE__Saliency__scaffold__seed1: FAILED list index out of range
- ShapeGGen__GINE__Saliency__scaffold__seed2: FAILED list index out of range
- ShapeGGen__GINE__InputXGradient__scaffold__seed0: FAILED list index out of range
- ShapeGGen__GINE__InputXGradient__scaffold__seed1: FAILED list index out of range
- ShapeGGen__GINE__InputXGradient__scaffold__seed2: FAILED list index out of range
- ShapeGGen__GINE__GuidedBackprop__scaffold__seed0: FAILED list index out of range
- ShapeGGen__GINE__GuidedBackprop__scaffold__seed1: FAILED list index out of range
- ShapeGGen__GINE__GuidedBackprop__scaffold__seed2: FAILED list index out of range
- ShapeGGen__GINE__GNNExplainer__scaffold__seed0: FAILED list index out of range
- ShapeGGen__GINE__GNNExplainer__scaffold__seed1: FAILED list index out of range
- ShapeGGen__GINE__GNNExplainer__scaffold__seed2: FAILED list index out of range
- ShapeGGen__GINE__PGExplainer__scaffold__seed0: FAILED list index out of range
- ShapeGGen__GINE__PGExplainer__scaffold__seed1: FAILED list index out of range
- ShapeGGen__GINE__PGExplainer__scaffold__seed2: FAILED list index out of range
- ShapeGGen__GINE__SubgraphX__scaffold__seed0: FAILED list index out of range
- ShapeGGen__GINE__SubgraphX__scaffold__seed1: FAILED list index out of range
- ShapeGGen__GINE__SubgraphX__scaffold__seed2: FAILED list index out of range
