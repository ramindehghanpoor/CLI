#! /usr/bin/env python

# Author: Ramin Dehghanpoor

# import libraries
import argparse
import numpy as np
from scipy.spatial import distance
import glob
from utils.io import read_fasta
from keras.models import model_from_json
from utils import aa_letters
from utils.data_loaders import to_one_hot
from keras import backend as K
import pandas as pd


def run(args):
    # get the arguments
    
    # First family
    n1 = args.first_family
    
    # Second family
    n2 = args.second_family
    
    # show names or not
    names_flag = args.show_names_bool
    
    #output_filename = args.output # from dest="output"
    
    # distance metric
    distance_metric = args.distance_metric # default is euclidean
    
    # The p-norm to apply for Minkowski
    p_norm = args.p_norm # default is 2
    
    # first new latent space
    nl1 = args.nl1 # default is ""
    
    # second new latent space
    nl2 = args.nl2 # default is ""
    
    # new sequence
    ns = args.ns # default is ""
    
    # set the distance metric
    if distance_metric == 'euclidean':
        distance_function = distance.euclidean
    elif distance_metric == 'minkowski':
        distance_function = distance.minkowski
    elif distance_metric == 'cityblock':
        distance_function = distance.cityblock
    elif distance_metric == 'sqeuclidean':
        distance_function = distance.sqeuclidean
    elif distance_metric == 'cosine':
        distance_function = distance.cosine
    elif distance_metric == 'correlation':
        distance_function = distance.correlation
    elif distance_metric == 'hamming':
        distance_function = distance.hamming
    elif distance_metric == 'jaccard':
        distance_function = distance.jaccard
    elif distance_metric == 'chebyshev':
        distance_function = distance.chebyshev
    elif distance_metric == 'canberra':
        distance_function = distance.canberra
    elif distance_metric == 'braycurtis':
        distance_function = distance.braycurtis
    elif distance_metric == 'yule':
        distance_function = distance.yule
    elif distance_metric == 'dice':
        distance_function = distance.dice
    elif distance_metric == 'kulsinski':
        distance_function = distance.kulsinski
    elif distance_metric == 'rogerstanimoto':
        distance_function = distance.rogerstanimoto
    elif distance_metric == 'russellrao':
        distance_function = distance.russellrao
    elif distance_metric == 'sokalmichener':
        distance_function = distance.sokalmichener
    elif distance_metric == 'sokalsneath':
        distance_function = distance.sokalsneath
    
    # when the user asks for the names of the proteins
    if names_flag:
        print('Here is a list of protein families\' names:\n')
        print('ATKA_ATKC, CDSA_RSEP, DHPS_FOLB, PHOU_PSTA, PTSO_YHBJ, MIAA_MUTL, ENVR_GLRX3, LPXD_RRF, COABC_NUSB, NDK_YFGM, WZB_YFEH, ZNUA_ZNUB, MOAB_MOAC, YBBO_YCEF, SYC_TRML, CLPX_TIG, BAMB_YFGM, ASTC_TAM, CORC_YAFV, ENTH_RHLB, CLPP_CLPX, THRC_TRPA, CHEA_CHEW, KHSE_YIHR, FRE_PYRB, LIPA_LIPB, KPRS_RMLA1, RRF_UPPS, METF_RFFA, DDLB_MRAY, CHPB_CHPS, ATPE_RHO, AMTB_GLNK, CCMC_NRFF, ISPB_UBIG, FLIF_FLIG, ATPD_ATPL, CUSA_CUSC, MOAC_MOAD, SKP_TAMA, CBRA_MAP1, HOLA_KTHY, FLGF_YAJR, HPF_YHBJ, HDA_YIDD, ISCA_ISCX, YGBL_YGBM, TATD_YGJH, ARGB_ARGD, ILVB_ILVN, YBFI_YHBU, YADG_YBHG, CSPD_IF1, PHOL_YBEY, FRE_PYRD, CSDA_YGDK, RISA_TADA, THID_THIM, EMRA_MPRA, BASS_YBFI, IDH_ILVN, YADG_YADH, RNFD_RNFG, CHEY_OTSB, CORC_YBEY, FIXA_MENE, GSA_HEM3, IF1_RPOA, PUR3_PUR5, ATPD_ATPG, HPF_LPTC, FTSW_MURC, RIBB_RISA, TDCB_YBIB, PTH_YCHF, FABH_PLSX, MAP1_RRF, GNTX_RFH, ACCC_PUR5, LPTC_PTSN, DEF_RSMB, GLCE_GLCF, HCAE_HCAF, GLRX3_SECB, CYSP_CYST, FLGD_FLGL, DHSB_DHSC, QOR2_YTFH, YEFM_YOEB, FRE_RNFG, FLIL_FLIP, YIAN_YIAO, HIS5_PHYDA, PNCC_RECX, RSMA_TATD, QUED_QUEE, PHOU_PSTS, LSPA_RIBF, PSPB_PSPC, QMCA_YBBJ, CCMB_CCME, ASSY_PYRB, FTSI_MRAY, HEM2_HEM4, MLAC_MLAD, RNH2_UPPS, PAAF_PAAH, RNFE_RNFG, HEM1_HEM2, PURE_PURK, ENGB_PDXJ, XDHA_XDHB, MLAE_YEHX, FABG_YCED, BCCP_FABZ, FRLB_MOCA, MDTN_MDTP, APT_PYRF, MTOX_THIS, IF1_LFTR, DEOR_PTFB1, ATP6_ATPL, FLGF_FLGK, RIMM_RNH2, DHPS_YHBY, ACCC_HOA, NUOJ_NUOK, BCSQ_RSMG, ACP_RNC, THIF_THIG, PAAB_YFAE, CDSA_UPPS, ACP_PABC, AROB_AROK, FLIL_FLIQ, ATOA_ATOD, PLDB_RHTB, CBPA_YGGW, CCMA_CCMB, ARGB_ARGC, PROA_PROB, ATPL_RMLA1, COAD_RSMD, NADD_YHBY, ATPD_ATPF, RNH2_SKP, AMPE_HIS8, HPPK_PANB, CHEY_YGIW, HOLC_LPTF, TOLR_YBGC, TUSB_TUSC, YCGM_YFCF, RLME_YHBY, PTPC2_YADI, ACP_YCEF, BCSQ_MNMG, ACPS_CHPB, EPMA_SYH, OBG_PYRH, GSPG_GSPJ, QUEA_YAJC, RATA_SSRP, RRF_RSEP, FABZ_PYRH, ATPE_MOCA, BETA_YBJK, COBC_COBU, SRP54_TRMD, NUOF_NUOJ, DIAA_YRAN, CHEB_CHEW, HEM1_HEM4, YAGP_YAHO, CYOC_NUOK, HIS4_HISX, PYRH_YIJO, EFTS_RSEP, GLGX_RMLA2, HPF_PTSN, AROB_AROC, FLHB_FLIQ, ENGB_YJEE, NIFU_YJFP, MOAD_MOAE, FER_ISCA, DAPE_PYRB, COAE_PPPA, CHEY_CHEZ, ARGB_ASSY, HDA_PUR3, DUSC_RIMK, NUOF_NUON, QUEC_QUEE, QUEA_TGT, ALSE_DEF, MIAB_PHOL, LSRB_NANK, MOCA_YAGQ, FLGC_FLGE, CLPP_DBHB, ENGB_QMCA, MLAC_MLAE, ULAA_ULAC, YEJB_YEJF, FRLB_RMLA1, HYBF_HYBG, FLGA_FLGD, RUTR_YIAV, CYSM_ISPE, NUOF_NUOK, NRFE_NRFF, NADD_RLMH, EAMB_YICL, NUOI_NUOK, FOLB_HPPK, DNAJ_DNAK, EUTD_TDCD, FTSI_MURE, MAP1_SECY, ATPD_RHO, PRMA_RSME, DHPS_GCH1, DEOR_PTFC2, KDSB_YCAR, RNH2_TRMD, NADA_NADC, ACP_FABD, TRPA_TRPB, TESB_YBBL, DPO3B_RECF, MURB_RODA, FLGD_FLGH, RIBA_TADA, FLIJ_FLIQ, RHLB_YADH, FER_MREB, NTRB_NTRC, MAP1_UPPS, MIOC_XERC, CYOA_CYOD, RIBF_RNPH, NRFF_NRFG, RIMM_TRMD, CYSQ_SERC, GUAC_PABA, ENGB_RODZ, FMT_YCIO, FLIE_FLIH, FOLC_MRAY, CYOC_CYOD, SLYX_TUSB, XDHB_XDHC, LSPA_RIMK, MNME_RNPA, ATPD_MOCA, YEBZ_YOBA, INSJ_INSO1, OSMF_YEHX, BIOC_GNTX, PTQA_PTQC, ISCA_ISCR, PRMC_RF1, RUVA_YBGC, ACCC_BCCP, RBSC_RBSD, NUOE_NUOL, TOLQ_TOLR, HCR_YRAR, FRE_PAAD, TGT_YAJC, MRAZ_MURE, FTSZ_MREB, RIBB_RISB, PABC_RLUA, ALDB_BETA, HIS5_HISX, DNAA_RNPA, CDSA_PYRH, CCMD_DSBE, DHPS_HPPK, PTGA_PTHP, SYGA_SYGB, MIAB_YBEY, FLIQ_FLIR, FLGA_FLGC, LSPA_SYI, MDTE_MDTF, IF1_KAD, DHPS_GREA, TATD_YIHX, KTHY_YCFH, CYSC_CYSD, LIPB_YBED, NUOE_NUOI, NUSB_RISB, YFJV_YGAV, FABG_PLSX, RBFA_RIBF, FLIE_FLIL, HYPC_HYPD, FOLC_SYC, THIE_THIS, HSCB_ISCA, HCAC_YFAE, GLNP_YEHX, FTSI_MURG, SECD_YAJC, LPXD_UPPS, GREA_YHBY, ERA_YBEY, LPTA_PTSN, YIAM_YIAO, HEM4_YQAB, CYOA_CYOC, AGAA_ALSK, FMT_RSMB, CLPP_PPIC, PPNK_RECN, ARGD_PYRB, AROK_HOFN, METI_NRDH, RIBA_RISB, YHCA_YHCD, ENGB_KDGL, PTPB1_PTPD, COBS_COBT, FTSI_MRAZ, FABH_FABZ, DKGA_METC, BGLG_PTGA, PNP_RBFA, PIMT_SURE, INSE1_INSF1, ALSB_RRAA, FABZ_LPXB, YAGQ_YAGS, PTFC2_PTSO, DIAA_YRAR, ACP_YCED, FABG_YCEG, FLGD_FLGE, YFIB_YJAB, CBPA_GRPE, FLIP_FLIQ, PUR1_THIL, APT_FRE, FLID_FLIS, RUVC_YEBC, HIS2_HIS8, ALKH_FRLD, PIMT_YGER, PRMC_YCIO, AVTA_SYN, MOAA_MOAE, HOLB_RECR, MOAC_MOEA, AAEX_YAGP, MMUM_RFFA, AGAA_AGAI, GNTX_HPF, FDOI_HYBD, MTOX_XYLB, CYOC_CYOE, TOLQ_YBGF, SAPC_SAPF, FABZ_SKP, FTSW_MRAZ, PDXJ_RNC, RIMO_YBEM, NUOA_NUOE, GCP_YEDL, NRDD_NRDG, MURI_RDGB, KTHY_YCEG, QUEC_QUED, ATPF_ATPL, FLGB_FLGE, ACP_FABF, YGFA_ZAPA, FABZ_LPXD, CBRA_YAFV, HIS2_HIS5, APPB_APPC, YIDC_YIDD, ENGB_LEP, RBSD_YEJF, MUTT_YGGR, KTHY_PABC, SYFA_TRML, FABF_FABZ, MRAY_MURG, ATPF_RMLA1, DNAA_DPO3B, COBT_COBU, RECA_RECX, BIOB_BIOD1, FEOA_YBFI, HCAC_HCAD, ACP_YCEG, BIOB_BIOF, YRAN_YRAP, HIS4_HIS8, MDLA_YBAO, FLGC_FLII, CLPS_LFTR, MREB_RODA, ACRE_ENVR, CCMA_CCMC, FABZ_TAMA, RNH2_YRDA, DAPF_XERC, CYOB_CYOC, RUVB_YEBC, METN_METQ, RIBB_TADA, FUR_ZNUB, MOAA_MOAB, GLGX_RFAB, RMLA1_RMLC, ARSR_YFEH, BGLB_PTGA, RIBF_TRUB, FLHB_FLIP, FLHA_FLHB, SECB_YIBN, ERA_RNC, FER_NIFU, PGSA_PNCC, DCUR_DCUS, ATPE_RMLA1, LPXA_SKP, MINC_MIND, PTQB_PTQC, PANC_PAND, CHEB_CHER, HCAF_YFAE, RLUE_XERD, IF1_MAP1, MRAY_MURF, CPXA_MACA, NIFU_TRML, FTSA_FTSZ, FOLB_PLSY, NUOI_NUOJ, END3_FETP, FABD_PLSX, FLHB_FLIR, HPF_LPTA, YBGJ_YBGK, ACP_RSUA, PTFB1_PTSO, ALSE_RSMB, ACP_BCCP, PYRB_PYRC, COAE_PPDD, PGSA_RECA, EFTS_FABZ, FECI_YFHL, ARSC_ARSR, ENGB_SYH, LOLC_TESA, NRDR_RIBD, LEU3_LEUD, FIME_HSLV, RNH2_YRAN, HFLX_MIAA, KPRS_PTH, RECO_RPOE, CLPP_TIG, ASSY_ASTC, 3MG2_OGT, FLIE_FLIN, ISCA_MREB, CCMA_CCMD, TESA_THIO, UMUC_UMUD, NUOH_NUON, CCMC_CCME, CCMD_NRFG, PTSO_YRBA, FLIL_FLIN, MOAA_MOAC, RNPA_YIDC, PGPA_THIL, RUVX_YCEG, END8_YBJK, IF3_SYT, NUOA_NUOF, DAPA_DAPB, DDLB_MURG, RUVA_RUVC, RECF_YBCJ, NUOF_NUOH, EFTS_RNH2, ISCA_NIFU, BISC_HCAD, CAIA_PAAH, CCMB_DSBE, PTPD_YADI, PANB_PANC, EFTS_UPPS, YIAM_YIAN, MREB_NIFU, PAAC_YFAE, HIGA_HIGB, DPO3B_GYRB, DKSA_HPPK, NLPC_YDIV, NUSB_THIL, TPX_YPJD, GREB_RIMI, CPDA_YDCV, FTSA_GRPE, GRPE_MREB, ENGB_GPDA, NUOE_NUOK, GLPF_GLPK, FECB_FECD, FLIJ_FLIL, ATP6_ATPE, NUSA_RIMP, IF1_SECY, YOHJ_YOHK, THIF_THIS, FLGC_FLGI, PPDD_YACG, YKGE_YKGF, HCAD_ODO2, CUSB_CUSC, DDPB_DDPC, LSPA_PABA, ILVI_LEU3, APT_SECF, FLIE_FLIO, FECI_FECR, NUOE_NUOJ, KDGL_RECO, YBHP_YCBL, MTOX_THIG, YDBL_YNBE, CCMD_CCME, XDHA_XDHC, LIVF_YGIN, ACCD_FOLC, FOLC_RODA, NADD_PYRH, NUDG_YDJA, PT1_PTHP, CYSD_CYSN, NUOA_NUOH, BAMB_ENGB, MENB_MEND, RIMK_RSME, TUSB_TUSD, MLAD_MLAE, THIH_THIS, EFG_EFTU1, PAAB_PAAC, MURB_MURG, GLRX1_TRML, SSUD_YIEF, TUSC_YCHN, IOJAP_YHBY, YBGK_YBGL, MOTA_MOTB, CCMA_LOLA, YBBA_YBBN, FTSW_RSMH, BCP_MSRB, BIOD1_CSDA, PTPC1_PTPD, ACP_SLYA, RUVB_RUVC, HPF_RFH, ACP_PLSX, FLAV_YBFF, PSTA_PSTS, SOXS_YMGE, CHAA_EVGA, PABA_PYRB, SLMA_YEES, KEFG_YTFH, SUFS_TAM, YBHR_YBIH, TOLR_YBGF, MUTT_YACG, YBHG_YBHR, ATPE_ATPG, ATP6_ATPF, GLPE_WCAB, HDA_YBCJ, CBRA_YDIQ, RATB_SSRP, YIAC_YJEE, PUR3_PUR9, TTDA_TTDB, TRPA_YBIB, ARGB_ARLY, NIKD_YCII, MOAA_MOBA, YFCQ_YRAH, MOAA_MOAD, CLPS_CSPD, FTSA_MRAY, ARGD_HEM4, FABD_FABH, BFD_BFR, HIS5_RSUA, FOLC_MUTT, EFTS_RRF, COAE_YACG, MLAC_YEHX, FABD_FABZ, PABA_SDHD, NUOA_NUOJ, DPO3E_RNH, PHNP_YCJY, DYR_TYSY, THIG_THIS, IF3_SYFA, ENGB_YFGM, BCSQ_MNME, SURE_YGER, RBFA_TRUB, LSRA_LSRB, FTSI_RSMH, OSMC_SLYA, NUSB_RIBB, ERA_PHOL, PANB_PAND, HIS4_HIS5, YEJA_YEJB, ISPE_PRMC, PHNK_YEJA, DEF_FMT, FER_ISCX, HSLU_HSLV, KBL_TDH, MRAY_RSMH, KHSE_RSMA, COAE_XNI, PNCC_RECA, KAD_MAP1, PROV_PROW, FTSA_FTSW, FLIM_FLIQ, NADD_PROA, YFHR_YIDA, MRAZ_RSMH, ATP6_ATPD, TAMA_UPPS, DPO3B_YIDD, FOLC_RIMK, DXS_EX7S, NSRR_TRML, ATPE_ATPF, ERPA_YGDK, PYRB_PYRI, CCMA_CCME, CYOC_HYCD, PAAC_PAAD, COBC_IOJAP, DNAC_YAGA, RIR1_RIR2, YNFH_YSAA, PABA_YBIB, PROW_PROX, HEM1_HEM3, ATPL_ATPZ, ATPF_MOCA, ERA_RECO, CH10_CH60, ACPS_ALR1, ACCC_PYRC, PGK_TPIS, FUCA_FUCK, ATKA_UHPA, CDSA_RRF, SFGH1_YGGP, SSRP_YBFF, YEAZ_YEDL, CDSA_LPXD, PSPE_YCJQ, FLIL_FLIR, HOFB_HOFC, DHSC_DHSD, ALSB_FOLC, PPIC_PRP1, PABA_PYRD, ARGR_PYRH, DEF_SMF, FTSW_MURG, ASCB_PTQB, DHPS_GLMM, MURC_MURG, FDNI_YSAA, HYFF_NUOI, COAE_MUTT, TOLB_TOLR, FLIE_FLIQ, CRCB_CSPE, SUCC_SUCD, HOLA_YBAB, ISPB_YHBE, NUSG_SECE, GCP_YJEE, RIDA_YCAC, RIMM_SRP54, TORD_YGFS, MIND_YGJH, SYFA_SYFB, FLIY_YECS, FLIA_PRIM, ATPD_ATPE, THIE_THIM, DBHA_PPIC, MNME_YIDD, RDGB_YFCE, GSPE_GSPG, DAPA_USG, ECPD_YADN, NSRR_SERC, RLUD_YFIH, PYRB_PYRD, MURG_RSMH, THID_THIS, CBRA_YCGM, NUOE_NUOF, PYRH_TAMA, AROA_KCY, RUVC_YBGC, COAE_YGGR, AAEX_YBHG, RISA_RISB, HOLA_PABC, DHSA_DHSB, YCED_YCEF, PABA_PABB, ENGB_PLSY, PYRD_RIMK, PHNH_PHNL, RUVA_YEBC, FLIL_FLIO, RBSA_RBSC, CUSC_EMRY, KHSE_MOCA, NUOH_NUOJ, MLAC_YRBA, RNFB_RNFE, DBHB_FADM, RUVX_YQGE, DDLB_LPXC, PTKA_PTKB, ARLY_ASSY, NRDR_RISA, PUR3_THIL, RIBD_RISB, PTMA_YHBJ, CCME_DSBE, DDLA_GREB, MNMA_SERC, ASCB_PTQA, YPHB_YPHE, HEM3_HEM4, MURE_RSMH, MLAB_PTSO, ARTM_YFAE, RNFD_RNFE, FLIA_YBGI, ENGB_KCY, FIMB_YIGA, HSCB_NIFU, HYPD_HYPE, IHFB_SERC, IF1_TRXB, GAL1_GALE, KDSB_LPXK, ACPS_FECI, DEF_RIMN, RSMI_YRAN, DDLB_RSMH, LPXD_PYRH, HYPA_HYPD, RFH_YCIO, FABZ_RRF, INSD8_INSJ, RECF_YIDD, COBC_COBS, ACRB_ACRR, OSMF_YEHW, GCP_YEAZ, KDGL_YBEY, PTFLB_YIHV, MREB_NSRR, FLIM_FLIR, BIOC_BIOF, GPH_RPE, FTSE_PHNG, FOLC_MURG, DPO3B_RNPA, GLPE_GPDA, THID_THIE, PPIC_RSMA, RECF_RNPA, PABB_YBIB, FER_ISCS, THIE_THIG, LEUC_LEUD, DUT_YEES, FTSB_ISPD, RISB_THIL, FRMR_GLPE, EMRB_MPRA, YDIO_YDIR, NAGA_NAGB, LSPA_RLUA, NRDH_NRDI, LPXH_PPIB, BCP_NRFG, MOBA_MOBB, GCSH_GCST, RNH_YAFS, YCIB_YCII, ZNUB_ZNUC, NUSB_RIBA, EFP_MAP1, CHEW_MCP2, RDGB_RNPH, NADB_NADC, MLAB_YRBA, FECI_RNC, FOLC_MREB, XDHC_YAGQ, GLO2_RNH, BAMD_RSUA, MLAD_YEHX, YDCT_YDCV, RSMI_TATD, FADM_YBAO, LNT_YBEY, PSPE_YGAV, PDXA_RSMA, HINT_PABA, GLO2_YFCA, NUOE_NUOH, PFLA_PFLB, HPF_KDSC, FRE_PAAB, GLGA_GLGC, MOAC_MOAE, BIOD1_BIOF, PARC_PARE, RSEP_UPPS, END3_YBJK, FLGB_FLGH, DNAA_RECF, FTSB_ISPF, BCP_DAPA, DINJ_YAFQ, CCMB_CCMC, SERC_WCAB, EPMA_RFH, GYRB_RECF, FLIN_FLIQ, LIVH_LIVK, FLGH_FLGI, LPXB_RRF, ACP_KTHY, FLGB_FLGI, ACP_HOLB, YBGJ_YBGL, C56I_YCEI, HDA_THIL, HIS5_YCIO, HPF_YRBA, CDSA_DXR, RNPA_YBCJ, APAG_PPIC, PYRH_UPPS, PUR7_PURE, CORC_PHOL, CHEY_YDDL, ACPS_PDXJ, KHSE_LOLB, ATZN_FRMR, HDA_PARE, LPXK_YCAR, FLGB_FLGD, MIND_MINE, MAP1_RPOA, GSPH_GSPI, EFTS_PYRH, YBGC_YBGF, HYAD_HYPC, CCME_NRFG, EX7S_ISPA, METI_METQ, FLIE_FLIJ, KDSC_PTHP, RRF_TAMA, CBPA_RSME, PTSN_YRBA, ACPS_ERA, PDXA_PPIC, FLIG_FLII, IOJAP_NADD, RECR_YBAB, CARA_CARB, FABG_KTHY, FEOA_FEOB, HEM2_HEM3, ALSE_RSGA, ACP_HOLA, CBPA_FTSA, ULAB_ULAF, DXR_RSEP, MARA_YGHB, CSIE_ULAB, DPO3B_YBCJ, GLRX3_YIBN, PYRH_RSEP, MOAB_MOAD, THRC_YBIB, RNPA_YIDD, BGLG_PTIBC, EAMB_RHLB, TOLB_YBGC, IF3_IHFA, CCMD_NRFF, RATA_RATB, GSPG_GSPK, SECG_TPIS, KDSC_LPTA, GSA_HEM2, EMRK_EMRY, HPF_PTSO, ENGB_NDK, GCST_MTOX, IOJAP_RLMH, DHPS_FTSH, LPTA_LPTC, ATPE_ATPL, PHOL_YAFV, RNFB_RNFD, ATPF_ATPG, G3P1_TPIS, MRAZ_MURG, FLIP_FLIR, CYSQ_TRML, PTQA_PTQB, END3_SLYA, KAD_RPOA, ATP6_ATPG, THIO_YPJD, SRMB_TRML, YDES_YDET, KHSE_RFH, YNFE_YNFG, ACPS_RNC, E4PD_PGK, BIOA_BIOF, NUSB_PGPA, MNMG_RSMG, G6PD_YIEK, NUSB_RISA, PAAH_PAAJ, MNME_RSMG, GLUQ_TRML, HOLB_YBAB, YBJG_YBJK, IHFB_KCY, CYOC_NUOM, RPOA_SECY, NUOK_NUOL, FER_ISCR, YJJB_YJJP, DXR_UPPS, KDSC_PTSN, SERA_SERC, MOAB_MOAE, MOAE_MOEA, XYLB_XYLH, THIE_YGDL, LSRB_RBSD, KDSC_KDSD, CHEY_CUTC, FABZ_RSEP, BIOH_GNTX, COBS_COBU, ALSB_ALSC, YGCQ_YGCR, PTH_RHLB, FLIO_FLIQ, AMIA_YJEE, CORC_GLTK, FABZ_UPPS, ETP_YCIO, ISPA_NUSB, ATPB_ATPG, PTPB1_PTPC1, PYRD_PYRE, FLGK_FLGL, DDLA_FTSZ, HOLA_RECR, ACP_FABZ, LOLC_MACA, CBRA_GHRB, NUSA_RBFA, RNFB_RNFG, DPIA_PGSA, KDSC_MLAF, PNP_TRUB, HSCB_ISCX, HEM4_HEMY, CDSA_EFTS, NLPC_YEHX, ACCC_PABA, FLIJ_FLIO, ASTC_THIH, AQPZ_MTOX, RIBF_RIMP, USPE_YEIL, NAGA_PURK, FLGC_FLGH, FABZ_RNH2, MINC_MINE, BCSQ_YFJY, LPXA_TAMA, ATPD_RMLA1, RIBA_RISA, CDSA_FABZ, HSCB_ISCR, DDLB_MRAZ, CLPX_ENGB, FOLB_GCH1, DXS_ISPA, DBHA_ULAD, HIS2_HIS4, BAME_RATB, ISCS_NIFU, GSPI_GSPJ, FLGH_FLGL, ISCR_NIFU, PAAB_PAAD, NUOJ_NUOL, GLPE_YFCA, PTFC2_PTMA, CAIA_FIXA, YEAZ_YJEE, IOJAP_OBG, BCP_NRFF, RPOE_WCAB, FLGB_FLGC, APT_DTD, PAL_YBGC, THIO_YJEE, GLO2_YAFS, HOLB_KTHY, TAUA_TAUC, PYRH_RRF, MLAD_YRBA, RUVA_RUVB, PAAD_YFAE, PSTS_YEHX, NNR_YJEE, TOLB_TOLQ, NUSB_RSGA, FLGA_FLGH, BGLB_BGLG, GSPF_GSPG, LEU3_LEUC, FRE_ULAD, PTSO_YADI, COABC_DUT, YNJB_YNJC, RHTA_YBIR, SECF_YAJC, YBHK_YHBJ, FLGC_FLGD, HYPC_HYPE, T1MK_T1SK, CYSQ_NSRR, KDSC_LPTC, PYRC_PYRD, HIS8_HISX, LPTA_PTSO, ISCA_TRML, FLIM_FLIP, YEJA_YEJE, RIMP_RRF, DHAK_DHAL, CBRA_YGCQ, FENR_YEAW, PROV_PROX, CCMC_DSBE, ARGB_PYRB, ACP_FADM, NRFC_NRFD, FLGA_FLGB, FTSW_MRAY, NUOA_NUOI, YEIE_YEIH, ACCC_PYRB, DPIA_RLUE, RDGB_YGGW, BIOC_BIOD1, RIMI_YHHW, GSPG_GSPI, NUOA_NUON, ACCC_PUR3, ARSR_WZB, CCME_NRFF, MRAY_MRAZ, KGUA_YICC, P5CR_YGGS, KPRS_MOCA, TOLQ_YBGC, KAD_SECY, ATPL_MOCA, ATPG_ATPL, FER_HSCB, FRE_GLTD, ISPD_ISPF, NIKC_YBDH, SKP_UPPS')
        return
    
    # when the user provides a new seuence, try to reconstruct this sequence with different trained networks that we have to find the network with the highest reconstruction accuracy.
    if (ns != ""):
        # read the new sequence from the file
        protein_seq_file = open(ns,"r+")
        protein_seq = protein_seq_file.read()
        # list of all the trained networks. Each trained network belongs to a specific family
        networks_list = glob.glob('Trained_networks/*.h5')

        # get Amino Acid letter from the one hot encoded version of it
        def get_AA(n):
            return list(aa_key.keys())[list(aa_key.values()).index(n)]
        aa_key = {l: i for i, l in enumerate(aa_letters)}

        max_acc = 0
        chosen_family = 'none'

        # get the sequence length for each protein family that we have
        seq_lengths = pd.read_csv('seq_lengths.csv',usecols=['name', 'size'])

        # loop over all the tained networks and find the one with highest reconstruction accuracy
        for i in range(0, len(seq_lengths)):
            test_seq = protein_seq
            
            # skip the families with shorter protein sequence length
            if int(seq_lengths['size'][i]) < len(test_seq):
                continue

            # load the trained network
            json_file = open('Trained_networks/' + seq_lengths['name'][i] + '.json', 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            loaded_model = model_from_json(loaded_model_json)

            #load weights into new model
            loaded_model.load_weights('Trained_networks/' + seq_lengths['name'][i] + '_weights.h5')
            
            #new_encoder = loaded_model.layers[1]
            #if int(loaded_model.layers[0].input_shape[1]/21) < len(test_seq):
            #    continue

            # add left and right gaps to get the same size sequence as the sequences used for training this network
            left_gaps = int((int(seq_lengths['size'][i]) - len(test_seq))/2)
            right_gaps = int(seq_lengths['size'][i]) - len(test_seq) - left_gaps
            test_seq = (left_gaps*'-') + test_seq + (right_gaps*'-')
            seq_length = len(test_seq)

            # use the one hot encoded version of the protein sequence
            single_msa_seq = [test_seq]
            x_test = to_one_hot(single_msa_seq)
            y_test = K.argmax(x_test, axis=-1)
            x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))

            # reconstruct the new protein sequence with the network
            a = loaded_model.predict(x_test, steps = 1)
            a = a.reshape(len(single_msa_seq),seq_length,21)
            
            # x is the reconstructed sequence
            x = np.vectorize(get_AA)(np.argmax(a, axis=-1))
            x = np.array(x).tolist()
            for k in range(0, len(x)):
                x[k] = ''.join(x[k])
            count = 0
            
            # find the reconstruction accuracy
            for j in range(0, len(x[0])):
                if x[0][j] == single_msa_seq[0][j]:
                    count = count + 1
            acc = count / len(x[0])
            
            # update the max accuracy and the chosen family name
            if acc > max_acc:
                max_acc = acc
                chosen_family = seq_lengths['name'][i]
        print('The closest protein family is ' + chosen_family + ' with average accuracy of ' + str(max_acc))
        
    
    # show the usage to the user
    elif (n1 == "" and (nl1 == "" and nl2 == "")) or (n2 == "" and (nl1 == "" and nl2 == "")):
        print('usage: compare_fingerprints.py [-h] [-n1 FIRST_FAMILY] [-n2 SECOND_FAMILY] [-names SHOW_NAMES_BOOL] [-m DISTANCE_METRIC] [-p P_NORM] [-nl1 NL1] [-nl2 NL2] [-ns NS]')        
        print('To see help: ./compare_fingerprints.py -h')
        return
        
    # when the user provides two latent spaces of the proteins that we have
    elif (n1 != "") and (n2 != ""):
        a1 = np.loadtxt('Latent_spaces/'+n1+'.txt')
        a2 = np.loadtxt('Latent_spaces/'+n2+'.txt')
        
    # when the user provides one new latent space and one from the proteins that we have
    elif n1 != "":
        a1 = np.loadtxt('Latent_spaces/'+n1+'.txt')
        if nl1 != "":
            a2 = np.loadtxt(nl1)
        else:
            a2 = np.loadtxt(nl2)
            
    elif n2 != "":
        a2 = np.loadtxt('Latent_spaces/'+n2+'.txt')
        if nl1 != "":
            a1 = np.loadtxt(nl1)
        else:
            a1 = np.loadtxt(nl2)
        
    # when the user provides only one new latent space and we want to find the closest latent space to that new one
    elif (nl1 != "") and (nl2 == ""):
        #find closest
        latent_space_list = glob.glob('Latent_spaces/*')
        a1 = np.loadtxt(nl1)
        min_dist = float("inf")
        for j in range(0, len(latent_space_list)):
            if distance_function(a1, np.loadtxt(latent_space_list[j])) < min_dist:
                min_dist = distance_function(a1, np.loadtxt(latent_space_list[j]))
                closest_family = latent_space_list[j]
        print('The closest protein family is ' + closest_family[14:len(closest_family)-4] + ' with ' + str(distance_function).split()[1] + ' distance: ' + str(min_dist))
        return
    
    elif (nl1 == "") and (nl2 != ""):
        #find closest
        latent_space_list = glob.glob('Latent_spaces/*')
        a2 = np.loadtxt(nl2)
        min_dist = float("inf")
        for j in range(0, len(latent_space_list)):
            if distance_function(a2, np.loadtxt(latent_space_list[j])) < min_dist:
                min_dist = distance_function(a2, np.loadtxt(latent_space_list[j]))
                closest_family = latent_space_list[j]
        print('The closest protein family is ' + closest_family[14:len(closest_family)-4] + ' with ' + str(distance_function).split()[1] + ' distance: ' + str(min_dist))
        return
    
    # when the user provides two new latent spaces
    else:
        a1 = np.loadtxt(nl1)
        a2 = np.loadtxt(nl2)

    # find distance between two vectors a1 and a2
    if (ns == ""):
        print(str(distance_function).split()[1] + ' distance: ' + str(distance_function(a1, a2)))
        
    
    
def main():
    parser=argparse.ArgumentParser(description='''Find the distance between fingerprints of two protein families. 
    
Available metrics: 
    euclidean, minkowski, cityblock, sqeuclidean, cosine, correlation, hamming, jaccard, chebyshev, canberra, braycurtis, yule, dice, kulsinski, rogerstanimoto, russellrao, sokalmichener, sokalsneath



To see all the available protein families, run command:
    ./compare_fingerprints.py -names 1
        
As an example you can find the Euclidean distance between two families ATKA_ATKC and CDSA_RSEP by running the command:
    ./compare_fingerprints.py -n1 ATKA_ATKC -n2 CDSA_RSEP
    
Or if you want to find the Cityblock distance between ATKA_ATKC and a new latent space stored at second_new_latent_example.txt, you can run the command:
    ./compare_fingerprints.py -n1 ATKA_ATKC -nl2 second_new_latent_example.txt -m cityblock
    
Or if you want to find the cosine distance between two new latent spaces stored at first_new_latent_example.txt and second_new_latent_example.txt, you can run the command:
    ./compare_fingerprints.py -nl1 first_new_latent_example.txt -nl2 second_new_latent_example.txt -m cityblock
    
Or you can find the closest protein family to first_new_latent_example.txt in cosine distance by running the command:
    ./compare_fingerprints.py -nl1 first_new_latent_example.txt -m cosine
    
Also you can find the closest family to a new protein sequence (for example new_sequence_example.txt) by running:
    ./compare_fingerprints.py -ns new_sequence_example.txt
    
    ''',
                                  formatter_class=argparse.RawTextHelpFormatter)
    #parser.add_argument('--argument', default=None, help=''' ''')
    parser.add_argument("-n1",help="First family's name" ,dest="first_family", type=str, default="")
    parser.add_argument("-n2",help="Second family's name" ,dest="second_family", type=str, default="")
    parser.add_argument("-names",help="Boolean, Show available protein family names" ,dest="show_names_bool", type=bool, default=0)
    #parser.add_argument("-out",help="fastq output filename" ,dest="output", type=str, required=True)
    parser.add_argument("-m",help="[optional] Distance metric. Default: euclidean" ,dest="distance_metric", type=str, default="euclidean")
    parser.add_argument("-p",help="[optional] Scalar, The p-norm to apply for Minkowski, weighted and unweighted. Default: 2" ,dest="p_norm", type=int, default=2)
    parser.add_argument("-nl1",help="[optional] The file name of the first new latent space. Provide a new protein family latent space to compare it with one of the existing protein families or with the second new latent space. The file should contain 30 floats, each float in a separate line. If only one of the nl1 and nl2 provided, the closest protein family to this new latent space will be shown." ,dest="nl1", type=str, default="")
    parser.add_argument("-nl2",help="[optional] The file name of the second new latent space. Provide a new protein family latent space to compare it with one of the existing protein families or with the first new latent space. The file should contain 30 floats, each float in a separate line. If only one of the nl1 and nl2 provided, the closest protein family to this new latent space will be shown." ,dest="nl2", type=str, default="")
    parser.add_argument("-ns",help="[optional] The name of the file containing a protein sequence. Provide a protein sequence to get the closest protein family for this sequence." ,dest="ns", type=str, default="")
    #parser.add_argument("-V",help="ndarray The variance vector for standardized Euclidean. Default: var(vstack([XA, XB]), axis=0, ddof=1)" ,dest="variance_vector", type=np.ndarray, default='None')
    #parser.add_argument("-VI",help="ndarray The inverse of the covariance matrix for Mahalanobis. Default: inv(cov(vstack([XA, XB].T))).T" ,dest="inverse_covariance", type=np.ndarray, default='None')
    parser.set_defaults(func=run)
    args=parser.parse_args()
    args.func(args)

if __name__=="__main__":
    main()