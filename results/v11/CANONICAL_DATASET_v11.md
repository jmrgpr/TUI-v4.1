# CANONICAL_DATASET_v11

Este manifiesto lista los CSV canónicos de la serie v11 (F0_baseline, F1_highrisk, F2_redteam, F3 y, cuando exista, F4) y excluye las copias archivadas en `results/v11/archived` para garantizar trazabilidad única.

El script `scripts/generate_canonical_dataset_v11.py` controla la selección de archivos y el cálculo de su hash sha256.

## Resumen por fase
- `F0_baseline`: 6 archivos canónicos.
- `F1_highrisk`: 30 archivos canónicos.
- `F2_redteam`: 30 archivos canónicos.
- `F3`: 80 archivos canónicos.
- `F4`: 0 archivos canónicos.

## Manifest general

| phase | agent | grid | risk | seed | path | sha256 |
| --- | --- | --- | --- | --- | --- | --- |
| F0_baseline | control | 16 | 0.5 | 42 | `results/v11/F0_baseline/grid16/risklow/control/grid16_risklow_seed42_v11_episodes.csv` | `1a77c26235aa4ae2357eb49983ad9fdf60fdf334d726a4ef6166a22a9c1bca6c` |
| F0_baseline | dqn_control | 16 | 0.5 | 42 | `results/v11/F0_baseline/grid16/risklow/dqn_control/grid16_risklow_seed42_v11_episodes.csv` | `fa1c1d80965ee683ce40ca800803a4840d6e5700860560a4d5a5a9424225366b` |
| F0_baseline | simbiosis | 16 | 0.5 | 42 | `results/v11/F0_baseline/grid16/risklow/simbiosis/grid16_risklow_seed42_v11_episodes.csv` | `44db3bf21ffa573176eb5cc8952d5b04ecc3357db0997642d858332e2cc28149` |
| F0_baseline | control | 8 | 0.5 | 42 | `results/v11/F0_baseline/grid8/risklow/control/grid8_risklow_seed42_v11_episodes.csv` | `ea0333f10728d183b281bb466b9f0080f4b9214b741a1e0bbaaef65d1457bfa9` |
| F0_baseline | dqn_control | 8 | 0.5 | 42 | `results/v11/F0_baseline/grid8/risklow/dqn_control/grid8_risklow_seed42_v11_episodes.csv` | `a8189c29eee497d3b9efaef105e3f61568295f66bac78685f80f2a86c4b352af` |
| F0_baseline | simbiosis | 8 | 0.5 | 42 | `results/v11/F0_baseline/grid8/risklow/simbiosis/grid8_risklow_seed42_v11_episodes.csv` | `d6b3367ff4348d454aec0d25e482e7b7971e13a1e3ab36ebd8d001ed38d8a804` |
| F1_highrisk | control | 16 | 1.2 | 101 | `results/v11/F1_highrisk/grid16/riskhigh/control/grid16_riskhigh_r1p2_seed101_v11_episodes.csv` | `23ebca4207062ced8903f5cf8069e5b9bacdd4a2cec7f902f17a5a6e6c18be6f` |
| F1_highrisk | control | 16 | 1.2 | 13 | `results/v11/F1_highrisk/grid16/riskhigh/control/grid16_riskhigh_r1p2_seed13_v11_episodes.csv` | `b3291b25a77dbe6f94253defd957b01738dc90bc16d66ed7a15f57a4fcf5049b` |
| F1_highrisk | control | 16 | 1.2 | 42 | `results/v11/F1_highrisk/grid16/riskhigh/control/grid16_riskhigh_r1p2_seed42_v11_episodes.csv` | `59c2b4e22d28d9db5f83f59afef7bebfce2ca4599358f2dc24ca78324e90d177` |
| F1_highrisk | control | 16 | 1.2 | 7 | `results/v11/F1_highrisk/grid16/riskhigh/control/grid16_riskhigh_r1p2_seed7_v11_episodes.csv` | `c8d6c62354c5668e480c022c96f5e380fcce3442c9ffb9809707bfea4f161ea4` |
| F1_highrisk | control | 16 | 1.2 | 99 | `results/v11/F1_highrisk/grid16/riskhigh/control/grid16_riskhigh_r1p2_seed99_v11_episodes.csv` | `bde3f6ce8540b8fd7789ca73828ed1cdad943676dd8c76c60d4610eb227d7ef5` |
| F1_highrisk | dqn_control | 16 | 1.2 | 101 | `results/v11/F1_highrisk/grid16/riskhigh/dqn_control/grid16_riskhigh_r1p2_seed101_v11_episodes.csv` | `abdd422f51500cea3464a73d47b77700d9372b859c246eb674469bc7833c3866` |
| F1_highrisk | dqn_control | 16 | 1.2 | 13 | `results/v11/F1_highrisk/grid16/riskhigh/dqn_control/grid16_riskhigh_r1p2_seed13_v11_episodes.csv` | `333b785d26c3c5ac1721982be5ddbb4e586e74f53de8de1b648de63353f18e0a` |
| F1_highrisk | dqn_control | 16 | 1.2 | 42 | `results/v11/F1_highrisk/grid16/riskhigh/dqn_control/grid16_riskhigh_r1p2_seed42_v11_episodes.csv` | `50d1a252880d179425badaae50293e0609c21bd0f94eb3ffa480ecf7e89e9147` |
| F1_highrisk | dqn_control | 16 | 1.2 | 7 | `results/v11/F1_highrisk/grid16/riskhigh/dqn_control/grid16_riskhigh_r1p2_seed7_v11_episodes.csv` | `9991fc459910613d5705a961d801bd8fd1d1b2a6464746f83f5ad5b795fafddb` |
| F1_highrisk | dqn_control | 16 | 1.2 | 99 | `results/v11/F1_highrisk/grid16/riskhigh/dqn_control/grid16_riskhigh_r1p2_seed99_v11_episodes.csv` | `ce043e0188fc800a26a6914d69f40dd661cc4d6aad57a0cdef7ada35514edfa2` |
| F1_highrisk | simbiosis | 16 | 1.2 | 101 | `results/v11/F1_highrisk/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_seed101_v11_episodes.csv` | `dd5c534676cd8ea9b11fb03dccf5491af3dcab817c7dd7743c5fe79a59e76963` |
| F1_highrisk | simbiosis | 16 | 1.2 | 13 | `results/v11/F1_highrisk/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_seed13_v11_episodes.csv` | `fe9cc5886bb65a3872f9c29ad5153749f05638319aa74fae24968b018d10dea1` |
| F1_highrisk | simbiosis | 16 | 1.2 | 42 | `results/v11/F1_highrisk/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_seed42_v11_episodes.csv` | `d29a9fde50bb20ec5e051a1e721390266c71d0b1559bb1618f83755c9eff9741` |
| F1_highrisk | simbiosis | 16 | 1.2 | 7 | `results/v11/F1_highrisk/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_seed7_v11_episodes.csv` | `f2b34542a868c1ac9509b0ee2220b92e0b8a4ee646a35bf0076a947024e08d06` |
| F1_highrisk | simbiosis | 16 | 1.2 | 99 | `results/v11/F1_highrisk/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_seed99_v11_episodes.csv` | `245c959f12edcbf206dd39296a1649fb2da3c081dc1f9d6fc39c347bfc90994a` |
| F1_highrisk | control | 8 | 1.2 | 101 | `results/v11/F1_highrisk/grid8/riskhigh/control/grid8_riskhigh_r1p2_seed101_v11_episodes.csv` | `bea11b3b1bfb2bfb5a87b539fca146a063b443d60c56d320e8a80f43e1922b4b` |
| F1_highrisk | control | 8 | 1.2 | 13 | `results/v11/F1_highrisk/grid8/riskhigh/control/grid8_riskhigh_r1p2_seed13_v11_episodes.csv` | `3e8359e2d74e3656ed5409125884504ddf6f25d03673ee543be89efadc554306` |
| F1_highrisk | control | 8 | 1.2 | 42 | `results/v11/F1_highrisk/grid8/riskhigh/control/grid8_riskhigh_r1p2_seed42_v11_episodes.csv` | `906a9fe67122a97995c5cca0832bc7bff873664f77c5263310d8ea8e33eaa773` |
| F1_highrisk | control | 8 | 1.2 | 7 | `results/v11/F1_highrisk/grid8/riskhigh/control/grid8_riskhigh_r1p2_seed7_v11_episodes.csv` | `4de0741693654424aef986bca6df1e5fdbfcdb2bc97b859b580d3e8c4217e432` |
| F1_highrisk | control | 8 | 1.2 | 99 | `results/v11/F1_highrisk/grid8/riskhigh/control/grid8_riskhigh_r1p2_seed99_v11_episodes.csv` | `d0a19d32b9ee43fb7dd936350edf980979278ab209b14d3c1d15cb4342e680fa` |
| F1_highrisk | dqn_control | 8 | 1.2 | 101 | `results/v11/F1_highrisk/grid8/riskhigh/dqn_control/grid8_riskhigh_r1p2_seed101_v11_episodes.csv` | `4ef759d781cb036b3a94158a29843ed2fb85b03707f51dda048d4684036d5298` |
| F1_highrisk | dqn_control | 8 | 1.2 | 13 | `results/v11/F1_highrisk/grid8/riskhigh/dqn_control/grid8_riskhigh_r1p2_seed13_v11_episodes.csv` | `c1e1c6988dde360656c9362f6605d3e5f8e0ff36ba00219170f0c9cbfa821cad` |
| F1_highrisk | dqn_control | 8 | 1.2 | 42 | `results/v11/F1_highrisk/grid8/riskhigh/dqn_control/grid8_riskhigh_r1p2_seed42_v11_episodes.csv` | `61e2b1990beb5f49552a43298204192d3452ec73add6f683731c33b503c4914d` |
| F1_highrisk | dqn_control | 8 | 1.2 | 7 | `results/v11/F1_highrisk/grid8/riskhigh/dqn_control/grid8_riskhigh_r1p2_seed7_v11_episodes.csv` | `48d484b928b944963470f30ac34a34ef2b9fdda43e0b33790891b4f32e962a07` |
| F1_highrisk | dqn_control | 8 | 1.2 | 99 | `results/v11/F1_highrisk/grid8/riskhigh/dqn_control/grid8_riskhigh_r1p2_seed99_v11_episodes.csv` | `64695f18df59e04e04058888e23270bfca88ab5fb038cf992564c849599dd264` |
| F1_highrisk | simbiosis | 8 | 1.2 | 101 | `results/v11/F1_highrisk/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_seed101_v11_episodes.csv` | `f540f99ac5ccdb8203cc4e362d08f79e1e9f4fb766950bc82b1427c5c623d6d5` |
| F1_highrisk | simbiosis | 8 | 1.2 | 13 | `results/v11/F1_highrisk/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_seed13_v11_episodes.csv` | `8c4265c3e1e9ac4bb03e9b0ea83d0d1e18744478ec828be211a03ba3d88f91e0` |
| F1_highrisk | simbiosis | 8 | 1.2 | 42 | `results/v11/F1_highrisk/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_seed42_v11_episodes.csv` | `8868f8dd819c7742b108b8df94b45ec835087d150e1012a07dd1a33deb6f303a` |
| F1_highrisk | simbiosis | 8 | 1.2 | 7 | `results/v11/F1_highrisk/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_seed7_v11_episodes.csv` | `ff3497d23e7046a817c404cb241cf82ddacf862c6c7a0319ff1ef01b047fd452` |
| F1_highrisk | simbiosis | 8 | 1.2 | 99 | `results/v11/F1_highrisk/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_seed99_v11_episodes.csv` | `bc6b9b9ce12fea64f45fe1f0342394ad09c3c2fe941580379a7c76a85d1c8384` |
| F2_redteam | control | 16 | 1.2 | 101 | `results/v11/F2_redteam/grid16/riskhigh/control/grid16_riskhigh_r1p2_seed101_v11_episodes.csv` | `3f15bbda165e235223413a063c4547ef2b4b52aa2c7c582875a17b3d0fc4dee0` |
| F2_redteam | control | 16 | 1.2 | 13 | `results/v11/F2_redteam/grid16/riskhigh/control/grid16_riskhigh_r1p2_seed13_v11_episodes.csv` | `71ca3f77054ddce8cf65b6150b53746a246c8f4bde0c84dda8e127faf4e999dd` |
| F2_redteam | control | 16 | 1.2 | 42 | `results/v11/F2_redteam/grid16/riskhigh/control/grid16_riskhigh_r1p2_seed42_v11_episodes.csv` | `5d3867f5a2918018d4502ac129a3edd45b2d36468913749f3bc5e1acf59fbfde` |
| F2_redteam | control | 16 | 1.2 | 7 | `results/v11/F2_redteam/grid16/riskhigh/control/grid16_riskhigh_r1p2_seed7_v11_episodes.csv` | `95d92ca21072000035a8bbdee3ad82db8ce19497b05b98b2b2c6b21e1d221de0` |
| F2_redteam | control | 16 | 1.2 | 99 | `results/v11/F2_redteam/grid16/riskhigh/control/grid16_riskhigh_r1p2_seed99_v11_episodes.csv` | `f1f378e0015680575f99f818a366401d9bc872a13e7b324480652da227d9ca63` |
| F2_redteam | dqn_control | 16 | 1.2 | 101 | `results/v11/F2_redteam/grid16/riskhigh/dqn_control/grid16_riskhigh_r1p2_seed101_v11_episodes.csv` | `6691f199f5b229a9e1b8ca86d4e1fefca09f6ac64cac7bad68958381d322c938` |
| F2_redteam | dqn_control | 16 | 1.2 | 13 | `results/v11/F2_redteam/grid16/riskhigh/dqn_control/grid16_riskhigh_r1p2_seed13_v11_episodes.csv` | `2033e792eafd482feea1b492809bbfadc7841f29d422f83b43e0dab5fdae2864` |
| F2_redteam | dqn_control | 16 | 1.2 | 42 | `results/v11/F2_redteam/grid16/riskhigh/dqn_control/grid16_riskhigh_r1p2_seed42_v11_episodes.csv` | `8fda922bdf65dfbfcff3c8507dd9c0dbe10c7b591fdc81b38e6d86450768cfb2` |
| F2_redteam | dqn_control | 16 | 1.2 | 7 | `results/v11/F2_redteam/grid16/riskhigh/dqn_control/grid16_riskhigh_r1p2_seed7_v11_episodes.csv` | `cac325b008a27d97626347b061201d48542f3691eb3e7cda1b0b814812523848` |
| F2_redteam | dqn_control | 16 | 1.2 | 99 | `results/v11/F2_redteam/grid16/riskhigh/dqn_control/grid16_riskhigh_r1p2_seed99_v11_episodes.csv` | `64ea9b02a11ebc3b94cbda8aedac833c9a467d89a000277f0294c82f4f72ae02` |
| F2_redteam | simbiosis | 16 | 1.2 | 101 | `results/v11/F2_redteam/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_seed101_v11_episodes.csv` | `07bec8c4cadd093605ba0910d6def3dc1aa1fc755e618fb7110b8cb8cbff0dbd` |
| F2_redteam | simbiosis | 16 | 1.2 | 13 | `results/v11/F2_redteam/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_seed13_v11_episodes.csv` | `25e81ac300cf44cc8dce020f32ed612eaeda1373b81ee9c15386dc182d9beff5` |
| F2_redteam | simbiosis | 16 | 1.2 | 42 | `results/v11/F2_redteam/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_seed42_v11_episodes.csv` | `b4e54e2f65e69bc588722d842de6893d1f05393451879f0b803b203ccf53e225` |
| F2_redteam | simbiosis | 16 | 1.2 | 7 | `results/v11/F2_redteam/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_seed7_v11_episodes.csv` | `daa8a920d3c521c7ac39fcbbc4a29ad7674be1f6b4f789502995f79b846be612` |
| F2_redteam | simbiosis | 16 | 1.2 | 99 | `results/v11/F2_redteam/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_seed99_v11_episodes.csv` | `ca541a0d70a240a015cf0aa4302dc0aa25f52902eb4cf2a99fbe3aec9068db40` |
| F2_redteam | control | 8 | 1.2 | 101 | `results/v11/F2_redteam/grid8/riskhigh/control/grid8_riskhigh_r1p2_seed101_v11_episodes.csv` | `7008f3e921e37dff2fffe8d99244b99fbdaeb864b80bfe1ed22fa41e8ccf3cac` |
| F2_redteam | control | 8 | 1.2 | 13 | `results/v11/F2_redteam/grid8/riskhigh/control/grid8_riskhigh_r1p2_seed13_v11_episodes.csv` | `1937d4730331ec3ae12e593d3181818971c49e39a177d6c470788f2d3455810a` |
| F2_redteam | control | 8 | 1.2 | 42 | `results/v11/F2_redteam/grid8/riskhigh/control/grid8_riskhigh_r1p2_seed42_v11_episodes.csv` | `bce8814aa33ad6f23738bb7e7e404030e65dfd244c5480ceff82e08b9f152139` |
| F2_redteam | control | 8 | 1.2 | 7 | `results/v11/F2_redteam/grid8/riskhigh/control/grid8_riskhigh_r1p2_seed7_v11_episodes.csv` | `9ca642e7eaa0deb34618b93a3eb547a414dfbdc346d937825c22cf8f4dfa72a7` |
| F2_redteam | control | 8 | 1.2 | 99 | `results/v11/F2_redteam/grid8/riskhigh/control/grid8_riskhigh_r1p2_seed99_v11_episodes.csv` | `f6806b3d764a8b411dbbb2ea11f603f6e6b43ca8885b1439bf8b6a6483a90c53` |
| F2_redteam | dqn_control | 8 | 1.2 | 101 | `results/v11/F2_redteam/grid8/riskhigh/dqn_control/grid8_riskhigh_r1p2_seed101_v11_episodes.csv` | `3480251e6029c0bb93aecc6afc5c10cf2697108d6453a79b50762c0ea2cf91eb` |
| F2_redteam | dqn_control | 8 | 1.2 | 13 | `results/v11/F2_redteam/grid8/riskhigh/dqn_control/grid8_riskhigh_r1p2_seed13_v11_episodes.csv` | `593c58776f6210c541c47c225c2dbea1a1b5d11034b7f9b8b3d974185bf918be` |
| F2_redteam | dqn_control | 8 | 1.2 | 42 | `results/v11/F2_redteam/grid8/riskhigh/dqn_control/grid8_riskhigh_r1p2_seed42_v11_episodes.csv` | `5665e2c2a4aa436f08be5bdb6c2d749c87a1dfdbee0b27951cfdd5c87068f467` |
| F2_redteam | dqn_control | 8 | 1.2 | 7 | `results/v11/F2_redteam/grid8/riskhigh/dqn_control/grid8_riskhigh_r1p2_seed7_v11_episodes.csv` | `5435281659b301440133b930bd36286a1e20d40c6eb8b95c5f56cfd95906ccb5` |
| F2_redteam | dqn_control | 8 | 1.2 | 99 | `results/v11/F2_redteam/grid8/riskhigh/dqn_control/grid8_riskhigh_r1p2_seed99_v11_episodes.csv` | `a3c8c8d64b12c9497916ac5cb90f9eee17d61a088a119367025b9c980719539c` |
| F2_redteam | simbiosis | 8 | 1.2 | 101 | `results/v11/F2_redteam/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_seed101_v11_episodes.csv` | `454579d5b728db194d5186500c8b47fe173d70da4f7c68405f989abca9d26773` |
| F2_redteam | simbiosis | 8 | 1.2 | 13 | `results/v11/F2_redteam/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_seed13_v11_episodes.csv` | `fc0cb2faa2d85855398944a2e10c77c58f51af583eb84be8aafc77eb8ce74c14` |
| F2_redteam | simbiosis | 8 | 1.2 | 42 | `results/v11/F2_redteam/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_seed42_v11_episodes.csv` | `da8649e96350386581f2c7615b16c1a8a2079387f05cab69faf67fe19666edd5` |
| F2_redteam | simbiosis | 8 | 1.2 | 7 | `results/v11/F2_redteam/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_seed7_v11_episodes.csv` | `c9ce597c8b9d8318facca0646a2e6eb199ba361e9f723fef8a5d3458d025ca25` |
| F2_redteam | simbiosis | 8 | 1.2 | 99 | `results/v11/F2_redteam/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_seed99_v11_episodes.csv` | `1130784ffd6cb1122bac83f951579ede008acbb00957dbcd0a5c8e39c607ba6c` |
| F3 | control | 16 | 1.2 | 101 | `results/v11/F3/F1_highrisk/grid16/riskhigh/control/grid16_riskhigh_r1p2_f1_seed101_m0p0_v11_episodes.csv` | `23ebca4207062ced8903f5cf8069e5b9bacdd4a2cec7f902f17a5a6e6c18be6f` |
| F3 | control | 16 | 1.2 | 13 | `results/v11/F3/F1_highrisk/grid16/riskhigh/control/grid16_riskhigh_r1p2_f1_seed13_m0p0_v11_episodes.csv` | `b3291b25a77dbe6f94253defd957b01738dc90bc16d66ed7a15f57a4fcf5049b` |
| F3 | control | 16 | 1.2 | 42 | `results/v11/F3/F1_highrisk/grid16/riskhigh/control/grid16_riskhigh_r1p2_f1_seed42_m0p0_v11_episodes.csv` | `59c2b4e22d28d9db5f83f59afef7bebfce2ca4599358f2dc24ca78324e90d177` |
| F3 | control | 16 | 1.2 | 7 | `results/v11/F3/F1_highrisk/grid16/riskhigh/control/grid16_riskhigh_r1p2_f1_seed7_m0p0_v11_episodes.csv` | `c8d6c62354c5668e480c022c96f5e380fcce3442c9ffb9809707bfea4f161ea4` |
| F3 | control | 16 | 1.2 | 99 | `results/v11/F3/F1_highrisk/grid16/riskhigh/control/grid16_riskhigh_r1p2_f1_seed99_m0p0_v11_episodes.csv` | `bde3f6ce8540b8fd7789ca73828ed1cdad943676dd8c76c60d4610eb227d7ef5` |
| F3 | dqn_control | 16 | 1.2 | 101 | `results/v11/F3/F1_highrisk/grid16/riskhigh/dqn_control/grid16_riskhigh_r1p2_f1_seed101_m0p0_v11_episodes.csv` | `abdd422f51500cea3464a73d47b77700d9372b859c246eb674469bc7833c3866` |
| F3 | dqn_control | 16 | 1.2 | 13 | `results/v11/F3/F1_highrisk/grid16/riskhigh/dqn_control/grid16_riskhigh_r1p2_f1_seed13_m0p0_v11_episodes.csv` | `333b785d26c3c5ac1721982be5ddbb4e586e74f53de8de1b648de63353f18e0a` |
| F3 | dqn_control | 16 | 1.2 | 42 | `results/v11/F3/F1_highrisk/grid16/riskhigh/dqn_control/grid16_riskhigh_r1p2_f1_seed42_m0p0_v11_episodes.csv` | `50d1a252880d179425badaae50293e0609c21bd0f94eb3ffa480ecf7e89e9147` |
| F3 | dqn_control | 16 | 1.2 | 7 | `results/v11/F3/F1_highrisk/grid16/riskhigh/dqn_control/grid16_riskhigh_r1p2_f1_seed7_m0p0_v11_episodes.csv` | `9991fc459910613d5705a961d801bd8fd1d1b2a6464746f83f5ad5b795fafddb` |
| F3 | dqn_control | 16 | 1.2 | 99 | `results/v11/F3/F1_highrisk/grid16/riskhigh/dqn_control/grid16_riskhigh_r1p2_f1_seed99_m0p0_v11_episodes.csv` | `ce043e0188fc800a26a6914d69f40dd661cc4d6aad57a0cdef7ada35514edfa2` |
| F3 | simbiosis | 16 | 1.2 | 101 | `results/v11/F3/F1_highrisk/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_f1_seed101_m0p0_v11_episodes.csv` | `67df86b210191c74793caa38ff4ca0b567870d53a52135afdc912b2248747e26` |
| F3 | simbiosis | 16 | 1.2 | 101 | `results/v11/F3/F1_highrisk/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_f1_seed101_m0p2_v11_episodes.csv` | `dd5c534676cd8ea9b11fb03dccf5491af3dcab817c7dd7743c5fe79a59e76963` |
| F3 | simbiosis | 16 | 1.2 | 13 | `results/v11/F3/F1_highrisk/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_f1_seed13_m0p0_v11_episodes.csv` | `9c76ee173a69cd6f13b4d1bf373eb56c5db86843d6bd6e83f994c46f4875b0fd` |
| F3 | simbiosis | 16 | 1.2 | 13 | `results/v11/F3/F1_highrisk/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_f1_seed13_m0p2_v11_episodes.csv` | `fe9cc5886bb65a3872f9c29ad5153749f05638319aa74fae24968b018d10dea1` |
| F3 | simbiosis | 16 | 1.2 | 42 | `results/v11/F3/F1_highrisk/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_f1_seed42_m0p0_v11_episodes.csv` | `fe194a6055216ce0bca7af3060fc53cbc2fe78890b7a983660ec3d34057970b8` |
| F3 | simbiosis | 16 | 1.2 | 42 | `results/v11/F3/F1_highrisk/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_f1_seed42_m0p2_v11_episodes.csv` | `d29a9fde50bb20ec5e051a1e721390266c71d0b1559bb1618f83755c9eff9741` |
| F3 | simbiosis | 16 | 1.2 | 7 | `results/v11/F3/F1_highrisk/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_f1_seed7_m0p0_v11_episodes.csv` | `502f81d84d7131c50f64cbf1db3d2b2b7687c396f77ffa67765aab66446f250d` |
| F3 | simbiosis | 16 | 1.2 | 7 | `results/v11/F3/F1_highrisk/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_f1_seed7_m0p2_v11_episodes.csv` | `f2b34542a868c1ac9509b0ee2220b92e0b8a4ee646a35bf0076a947024e08d06` |
| F3 | simbiosis | 16 | 1.2 | 99 | `results/v11/F3/F1_highrisk/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_f1_seed99_m0p0_v11_episodes.csv` | `a0d992c21998afa068285182cc5098f494c202f84433410cbfb2ca4aaec10c65` |
| F3 | simbiosis | 16 | 1.2 | 99 | `results/v11/F3/F1_highrisk/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_f1_seed99_m0p2_v11_episodes.csv` | `245c959f12edcbf206dd39296a1649fb2da3c081dc1f9d6fc39c347bfc90994a` |
| F3 | control | 8 | 1.2 | 101 | `results/v11/F3/F1_highrisk/grid8/riskhigh/control/grid8_riskhigh_r1p2_f1_seed101_m0p0_v11_episodes.csv` | `bea11b3b1bfb2bfb5a87b539fca146a063b443d60c56d320e8a80f43e1922b4b` |
| F3 | control | 8 | 1.2 | 13 | `results/v11/F3/F1_highrisk/grid8/riskhigh/control/grid8_riskhigh_r1p2_f1_seed13_m0p0_v11_episodes.csv` | `3e8359e2d74e3656ed5409125884504ddf6f25d03673ee543be89efadc554306` |
| F3 | control | 8 | 1.2 | 42 | `results/v11/F3/F1_highrisk/grid8/riskhigh/control/grid8_riskhigh_r1p2_f1_seed42_m0p0_v11_episodes.csv` | `906a9fe67122a97995c5cca0832bc7bff873664f77c5263310d8ea8e33eaa773` |
| F3 | control | 8 | 1.2 | 7 | `results/v11/F3/F1_highrisk/grid8/riskhigh/control/grid8_riskhigh_r1p2_f1_seed7_m0p0_v11_episodes.csv` | `4de0741693654424aef986bca6df1e5fdbfcdb2bc97b859b580d3e8c4217e432` |
| F3 | control | 8 | 1.2 | 99 | `results/v11/F3/F1_highrisk/grid8/riskhigh/control/grid8_riskhigh_r1p2_f1_seed99_m0p0_v11_episodes.csv` | `d0a19d32b9ee43fb7dd936350edf980979278ab209b14d3c1d15cb4342e680fa` |
| F3 | dqn_control | 8 | 1.2 | 101 | `results/v11/F3/F1_highrisk/grid8/riskhigh/dqn_control/grid8_riskhigh_r1p2_f1_seed101_m0p0_v11_episodes.csv` | `4ef759d781cb036b3a94158a29843ed2fb85b03707f51dda048d4684036d5298` |
| F3 | dqn_control | 8 | 1.2 | 13 | `results/v11/F3/F1_highrisk/grid8/riskhigh/dqn_control/grid8_riskhigh_r1p2_f1_seed13_m0p0_v11_episodes.csv` | `c1e1c6988dde360656c9362f6605d3e5f8e0ff36ba00219170f0c9cbfa821cad` |
| F3 | dqn_control | 8 | 1.2 | 42 | `results/v11/F3/F1_highrisk/grid8/riskhigh/dqn_control/grid8_riskhigh_r1p2_f1_seed42_m0p0_v11_episodes.csv` | `61e2b1990beb5f49552a43298204192d3452ec73add6f683731c33b503c4914d` |
| F3 | dqn_control | 8 | 1.2 | 7 | `results/v11/F3/F1_highrisk/grid8/riskhigh/dqn_control/grid8_riskhigh_r1p2_f1_seed7_m0p0_v11_episodes.csv` | `48d484b928b944963470f30ac34a34ef2b9fdda43e0b33790891b4f32e962a07` |
| F3 | dqn_control | 8 | 1.2 | 99 | `results/v11/F3/F1_highrisk/grid8/riskhigh/dqn_control/grid8_riskhigh_r1p2_f1_seed99_m0p0_v11_episodes.csv` | `64695f18df59e04e04058888e23270bfca88ab5fb038cf992564c849599dd264` |
| F3 | simbiosis | 8 | 1.2 | 101 | `results/v11/F3/F1_highrisk/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_f1_seed101_m0p0_v11_episodes.csv` | `02d319ec1a1f1c6fcc475fdcb21b5bc26be1ae8c6ad5d27ead232b38be573c2d` |
| F3 | simbiosis | 8 | 1.2 | 101 | `results/v11/F3/F1_highrisk/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_f1_seed101_m0p2_v11_episodes.csv` | `f540f99ac5ccdb8203cc4e362d08f79e1e9f4fb766950bc82b1427c5c623d6d5` |
| F3 | simbiosis | 8 | 1.2 | 13 | `results/v11/F3/F1_highrisk/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_f1_seed13_m0p0_v11_episodes.csv` | `42681f26ca74a9cc626ecb385769311f9b6c1b712348c21b70c17cf171eab0d6` |
| F3 | simbiosis | 8 | 1.2 | 13 | `results/v11/F3/F1_highrisk/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_f1_seed13_m0p2_v11_episodes.csv` | `8c4265c3e1e9ac4bb03e9b0ea83d0d1e18744478ec828be211a03ba3d88f91e0` |
| F3 | simbiosis | 8 | 1.2 | 42 | `results/v11/F3/F1_highrisk/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_f1_seed42_m0p0_v11_episodes.csv` | `3389331913825b7b31d7341faf704cec03cc03269f0b93e1ca685bb3631564b9` |
| F3 | simbiosis | 8 | 1.2 | 42 | `results/v11/F3/F1_highrisk/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_f1_seed42_m0p2_v11_episodes.csv` | `8868f8dd819c7742b108b8df94b45ec835087d150e1012a07dd1a33deb6f303a` |
| F3 | simbiosis | 8 | 1.2 | 7 | `results/v11/F3/F1_highrisk/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_f1_seed7_m0p0_v11_episodes.csv` | `7f07873da36829be687826bfc1ba4f993188d09cf37942a0e6fcb654f71fac03` |
| F3 | simbiosis | 8 | 1.2 | 7 | `results/v11/F3/F1_highrisk/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_f1_seed7_m0p2_v11_episodes.csv` | `ff3497d23e7046a817c404cb241cf82ddacf862c6c7a0319ff1ef01b047fd452` |
| F3 | simbiosis | 8 | 1.2 | 99 | `results/v11/F3/F1_highrisk/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_f1_seed99_m0p0_v11_episodes.csv` | `ef159605a3311e15bc14e8352133048ff896239d5a836d49f47519f78e717e01` |
| F3 | simbiosis | 8 | 1.2 | 99 | `results/v11/F3/F1_highrisk/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_f1_seed99_m0p2_v11_episodes.csv` | `bc6b9b9ce12fea64f45fe1f0342394ad09c3c2fe941580379a7c76a85d1c8384` |
| F3 | control | 16 | 1.2 | 101 | `results/v11/F3/F2_redteam/grid16/riskhigh/control/grid16_riskhigh_r1p2_f2rt0p1_seed101_m0p0_v11_episodes.csv` | `3f15bbda165e235223413a063c4547ef2b4b52aa2c7c582875a17b3d0fc4dee0` |
| F3 | control | 16 | 1.2 | 13 | `results/v11/F3/F2_redteam/grid16/riskhigh/control/grid16_riskhigh_r1p2_f2rt0p1_seed13_m0p0_v11_episodes.csv` | `71ca3f77054ddce8cf65b6150b53746a246c8f4bde0c84dda8e127faf4e999dd` |
| F3 | control | 16 | 1.2 | 42 | `results/v11/F3/F2_redteam/grid16/riskhigh/control/grid16_riskhigh_r1p2_f2rt0p1_seed42_m0p0_v11_episodes.csv` | `5d3867f5a2918018d4502ac129a3edd45b2d36468913749f3bc5e1acf59fbfde` |
| F3 | control | 16 | 1.2 | 7 | `results/v11/F3/F2_redteam/grid16/riskhigh/control/grid16_riskhigh_r1p2_f2rt0p1_seed7_m0p0_v11_episodes.csv` | `95d92ca21072000035a8bbdee3ad82db8ce19497b05b98b2b2c6b21e1d221de0` |
| F3 | control | 16 | 1.2 | 99 | `results/v11/F3/F2_redteam/grid16/riskhigh/control/grid16_riskhigh_r1p2_f2rt0p1_seed99_m0p0_v11_episodes.csv` | `f1f378e0015680575f99f818a366401d9bc872a13e7b324480652da227d9ca63` |
| F3 | dqn_control | 16 | 1.2 | 101 | `results/v11/F3/F2_redteam/grid16/riskhigh/dqn_control/grid16_riskhigh_r1p2_f2rt0p1_seed101_m0p0_v11_episodes.csv` | `6691f199f5b229a9e1b8ca86d4e1fefca09f6ac64cac7bad68958381d322c938` |
| F3 | dqn_control | 16 | 1.2 | 13 | `results/v11/F3/F2_redteam/grid16/riskhigh/dqn_control/grid16_riskhigh_r1p2_f2rt0p1_seed13_m0p0_v11_episodes.csv` | `2033e792eafd482feea1b492809bbfadc7841f29d422f83b43e0dab5fdae2864` |
| F3 | dqn_control | 16 | 1.2 | 42 | `results/v11/F3/F2_redteam/grid16/riskhigh/dqn_control/grid16_riskhigh_r1p2_f2rt0p1_seed42_m0p0_v11_episodes.csv` | `8fda922bdf65dfbfcff3c8507dd9c0dbe10c7b591fdc81b38e6d86450768cfb2` |
| F3 | dqn_control | 16 | 1.2 | 7 | `results/v11/F3/F2_redteam/grid16/riskhigh/dqn_control/grid16_riskhigh_r1p2_f2rt0p1_seed7_m0p0_v11_episodes.csv` | `cac325b008a27d97626347b061201d48542f3691eb3e7cda1b0b814812523848` |
| F3 | dqn_control | 16 | 1.2 | 99 | `results/v11/F3/F2_redteam/grid16/riskhigh/dqn_control/grid16_riskhigh_r1p2_f2rt0p1_seed99_m0p0_v11_episodes.csv` | `64ea9b02a11ebc3b94cbda8aedac833c9a467d89a000277f0294c82f4f72ae02` |
| F3 | simbiosis | 16 | 1.2 | 101 | `results/v11/F3/F2_redteam/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_f2rt0p1_seed101_m0p0_v11_episodes.csv` | `2f4b44a886084033c9c05db0282c3855c8544eab463e25a45249f643eb7a91ad` |
| F3 | simbiosis | 16 | 1.2 | 101 | `results/v11/F3/F2_redteam/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_f2rt0p1_seed101_m0p2_v11_episodes.csv` | `07bec8c4cadd093605ba0910d6def3dc1aa1fc755e618fb7110b8cb8cbff0dbd` |
| F3 | simbiosis | 16 | 1.2 | 13 | `results/v11/F3/F2_redteam/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_f2rt0p1_seed13_m0p0_v11_episodes.csv` | `f33b87544321be3a7633619e6377652241d9a467d8862b2b0f5c21beffb1b855` |
| F3 | simbiosis | 16 | 1.2 | 13 | `results/v11/F3/F2_redteam/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_f2rt0p1_seed13_m0p2_v11_episodes.csv` | `25e81ac300cf44cc8dce020f32ed612eaeda1373b81ee9c15386dc182d9beff5` |
| F3 | simbiosis | 16 | 1.2 | 42 | `results/v11/F3/F2_redteam/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_f2rt0p1_seed42_m0p0_v11_episodes.csv` | `b248d39a60a5d5114512353cccf9261c1202b447450c3d0ab5a43f66d5ad893d` |
| F3 | simbiosis | 16 | 1.2 | 42 | `results/v11/F3/F2_redteam/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_f2rt0p1_seed42_m0p2_v11_episodes.csv` | `b4e54e2f65e69bc588722d842de6893d1f05393451879f0b803b203ccf53e225` |
| F3 | simbiosis | 16 | 1.2 | 7 | `results/v11/F3/F2_redteam/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_f2rt0p1_seed7_m0p0_v11_episodes.csv` | `4fa5de05bc0ade1a435cf0305dab238115982d79c120382558d02c3f8791a1c8` |
| F3 | simbiosis | 16 | 1.2 | 7 | `results/v11/F3/F2_redteam/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_f2rt0p1_seed7_m0p2_v11_episodes.csv` | `daa8a920d3c521c7ac39fcbbc4a29ad7674be1f6b4f789502995f79b846be612` |
| F3 | simbiosis | 16 | 1.2 | 99 | `results/v11/F3/F2_redteam/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_f2rt0p1_seed99_m0p0_v11_episodes.csv` | `78e0617bc8d0be739df1a81063bf4d68673f20d4b1eb69e6d5328716d45cb984` |
| F3 | simbiosis | 16 | 1.2 | 99 | `results/v11/F3/F2_redteam/grid16/riskhigh/simbiosis/grid16_riskhigh_r1p2_f2rt0p1_seed99_m0p2_v11_episodes.csv` | `ca541a0d70a240a015cf0aa4302dc0aa25f52902eb4cf2a99fbe3aec9068db40` |
| F3 | control | 8 | 1.2 | 101 | `results/v11/F3/F2_redteam/grid8/riskhigh/control/grid8_riskhigh_r1p2_f2rt0p1_seed101_m0p0_v11_episodes.csv` | `7008f3e921e37dff2fffe8d99244b99fbdaeb864b80bfe1ed22fa41e8ccf3cac` |
| F3 | control | 8 | 1.2 | 13 | `results/v11/F3/F2_redteam/grid8/riskhigh/control/grid8_riskhigh_r1p2_f2rt0p1_seed13_m0p0_v11_episodes.csv` | `1937d4730331ec3ae12e593d3181818971c49e39a177d6c470788f2d3455810a` |
| F3 | control | 8 | 1.2 | 42 | `results/v11/F3/F2_redteam/grid8/riskhigh/control/grid8_riskhigh_r1p2_f2rt0p1_seed42_m0p0_v11_episodes.csv` | `bce8814aa33ad6f23738bb7e7e404030e65dfd244c5480ceff82e08b9f152139` |
| F3 | control | 8 | 1.2 | 7 | `results/v11/F3/F2_redteam/grid8/riskhigh/control/grid8_riskhigh_r1p2_f2rt0p1_seed7_m0p0_v11_episodes.csv` | `9ca642e7eaa0deb34618b93a3eb547a414dfbdc346d937825c22cf8f4dfa72a7` |
| F3 | control | 8 | 1.2 | 99 | `results/v11/F3/F2_redteam/grid8/riskhigh/control/grid8_riskhigh_r1p2_f2rt0p1_seed99_m0p0_v11_episodes.csv` | `f6806b3d764a8b411dbbb2ea11f603f6e6b43ca8885b1439bf8b6a6483a90c53` |
| F3 | dqn_control | 8 | 1.2 | 101 | `results/v11/F3/F2_redteam/grid8/riskhigh/dqn_control/grid8_riskhigh_r1p2_f2rt0p1_seed101_m0p0_v11_episodes.csv` | `3480251e6029c0bb93aecc6afc5c10cf2697108d6453a79b50762c0ea2cf91eb` |
| F3 | dqn_control | 8 | 1.2 | 13 | `results/v11/F3/F2_redteam/grid8/riskhigh/dqn_control/grid8_riskhigh_r1p2_f2rt0p1_seed13_m0p0_v11_episodes.csv` | `593c58776f6210c541c47c225c2dbea1a1b5d11034b7f9b8b3d974185bf918be` |
| F3 | dqn_control | 8 | 1.2 | 42 | `results/v11/F3/F2_redteam/grid8/riskhigh/dqn_control/grid8_riskhigh_r1p2_f2rt0p1_seed42_m0p0_v11_episodes.csv` | `5665e2c2a4aa436f08be5bdb6c2d749c87a1dfdbee0b27951cfdd5c87068f467` |
| F3 | dqn_control | 8 | 1.2 | 7 | `results/v11/F3/F2_redteam/grid8/riskhigh/dqn_control/grid8_riskhigh_r1p2_f2rt0p1_seed7_m0p0_v11_episodes.csv` | `5435281659b301440133b930bd36286a1e20d40c6eb8b95c5f56cfd95906ccb5` |
| F3 | dqn_control | 8 | 1.2 | 99 | `results/v11/F3/F2_redteam/grid8/riskhigh/dqn_control/grid8_riskhigh_r1p2_f2rt0p1_seed99_m0p0_v11_episodes.csv` | `a3c8c8d64b12c9497916ac5cb90f9eee17d61a088a119367025b9c980719539c` |
| F3 | simbiosis | 8 | 1.2 | 101 | `results/v11/F3/F2_redteam/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_f2rt0p1_seed101_m0p0_v11_episodes.csv` | `029ce8f8698fdfac8cdfb2c81594e308dba2c73389ac5783fc81e32f8dd41216` |
| F3 | simbiosis | 8 | 1.2 | 101 | `results/v11/F3/F2_redteam/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_f2rt0p1_seed101_m0p2_v11_episodes.csv` | `454579d5b728db194d5186500c8b47fe173d70da4f7c68405f989abca9d26773` |
| F3 | simbiosis | 8 | 1.2 | 13 | `results/v11/F3/F2_redteam/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_f2rt0p1_seed13_m0p0_v11_episodes.csv` | `45f3543e246adffce343c8125134958680d12467b7d44671035279491664016a` |
| F3 | simbiosis | 8 | 1.2 | 13 | `results/v11/F3/F2_redteam/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_f2rt0p1_seed13_m0p2_v11_episodes.csv` | `fc0cb2faa2d85855398944a2e10c77c58f51af583eb84be8aafc77eb8ce74c14` |
| F3 | simbiosis | 8 | 1.2 | 42 | `results/v11/F3/F2_redteam/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_f2rt0p1_seed42_m0p0_v11_episodes.csv` | `7141050d1b288c3406d8105a662c067db4c6f8e78b8179cc1e25cc6d42e5509b` |
| F3 | simbiosis | 8 | 1.2 | 42 | `results/v11/F3/F2_redteam/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_f2rt0p1_seed42_m0p2_v11_episodes.csv` | `da8649e96350386581f2c7615b16c1a8a2079387f05cab69faf67fe19666edd5` |
| F3 | simbiosis | 8 | 1.2 | 7 | `results/v11/F3/F2_redteam/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_f2rt0p1_seed7_m0p0_v11_episodes.csv` | `e7e4a912fb2fc116fd95e7cd95bdaebdaa828670ebacae6236fb18b7b88a902e` |
| F3 | simbiosis | 8 | 1.2 | 7 | `results/v11/F3/F2_redteam/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_f2rt0p1_seed7_m0p2_v11_episodes.csv` | `c9ce597c8b9d8318facca0646a2e6eb199ba361e9f723fef8a5d3458d025ca25` |
| F3 | simbiosis | 8 | 1.2 | 99 | `results/v11/F3/F2_redteam/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_f2rt0p1_seed99_m0p0_v11_episodes.csv` | `35b68d5785c7c0654372b7abb4b9519009076cc4f72dab23f550d28958501c59` |
| F3 | simbiosis | 8 | 1.2 | 99 | `results/v11/F3/F2_redteam/grid8/riskhigh/simbiosis/grid8_riskhigh_r1p2_f2rt0p1_seed99_m0p2_v11_episodes.csv` | `1130784ffd6cb1122bac83f951579ede008acbb00957dbcd0a5c8e39c607ba6c` |

Se documenta adicionalmente en `results/v11/data/f2_vs_f1_diff.md` la comparativa F1 vs F2 y los campos meta `phase/attack_*` que enriquecen cada JSON.
Los archivos `raw/` y las copias en `archived/` solo se conservan para auditoría histórica; no se usan en análisis estadístico.