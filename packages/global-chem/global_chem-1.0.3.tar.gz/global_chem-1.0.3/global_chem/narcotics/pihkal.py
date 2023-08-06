#!/usr/bin/env python3
#
# GlobalChem - PiHKal
#
# -----------------------------------

class PihKal(object):

    def __init__(self):

        pass

    def get_functional_group_smiles(self):

        smiles = {
            1	AEM	alpha-Ethyl-3,4,5-trimethoxy-PEA
        2	AL	4-Allyloxy-3,5-dimethoxy-PEA
        3	ALEPH	4-Methylthio-2,5-dimethoxy-A
        4	ALEPH-2	4-Ethylthio-2,5-dimethoxy-A
        5	ALEPH-4	4-Isopropylthio-2,5-dimethoxy-A
        6	ALEPH-6	4-Phenylthio-2,5-dimethoxy-A
        7	ALEPH-7	4-Propylthio-2,5-dimethoxy-A
        8	ARIADNE (Dimoxamine)	2,5-Dimethoxy-alpha-ethyl-4-methyl-PEA
        9	ASB	3,4-Diethoxy-5-methoxy-PEA
        10	B	4-Butoxy-3,5-dimethoxy-PEA
        11	BEATRICE	2,5-Dimethoxy-4,N-dimethyl-A
        12	Bis-TOM	2,5-Bismethylthio-4-methyl-A
        13	BOB	4-Bromo-2,5,beta-trimethoxy-PEA
        14	BOD	2,5,beta-Trimethoxy-4-methyl-PEA
        15	BOH	beta-Methoxy-3,4-methylenedioxy-PEA
        16	BOHD	2,5-Dimethoxy-beta-hydroxy-4-methyl-PEA
        17	BOM	3,4,5,beta-Tetramethoxy-PEA
        18	4-Br-3,5-DMA	4-Bromo-3,5-dimethoxy-A
        19	2-Br-4,5-MDA	2-Bromo-4,5-methylenedioxy-A
        20	2C-B	4-Bromo-2,5-dimethoxy-PEA
        21	3C-BZ	4-Benzyloxy-3,5-dimethoxy-A
        22	2C-C	4-Chloro-2,5-dimethoxy-PEA
        23	2C-D	4-Methyl-2,5-dimethoxy-PEA
        24	2C-E	4-Ethyl-2,5-dimethoxy-PEA
        25	3C-E	4-Ethoxy-3,5-dimethoxy-A
        26	2C-F	4-Fluoro-2,5-dimethoxy-PEA
        27	2C-G	3,4-Dimethyl-2,5-dimethoxy-PEA
        28	2C-G-3	3,4-Trimethylene-2,5-dimethoxy-PEA
        29	2C-G-4	3,4-Tetramethylene-2,5-dimethoxy-PEA
        30	2C-G-5	3,4-Norbornyl-2,5-dimethoxy-PEA
        31	2C-G-N	1,4-Dimethoxynaphthyl-2-ethylamine
        32	2C-H	2,5-Dimethoxy-PEA
        33	2C-I	4-Iodo-2,5-dimethoxy-PEA
        34	2C-N	4-Nitro-2,5-dimethoxy-PEA
        35	2C-O-4	4-Isopropoxy-2,5-dimethoxy-PEA
        36	2C-P	4-Propyl-2,5-dimethoxy-PEA
        37	CPM	4-Cyclopropylmethoxy-3,5-dimethoxy-PEA
        38	2C-Se	4-Methylseleno-2,5-dimethoxy-PEA
        39	2C-T	4-Methylthio-2,5-dimethoxy-PEA
        40	2C-T-2	4-Ethylthio-2,5-dimethoxy-PEA
        41	2C-T-4	4-Isopropylthio-2,5-dimethoxy-PEA
        42	psi-2C-T-4	4-Isopropylthio-2,6-dimethoxy-PEA
        43	2C-T-7	4-Propylthio-2,5-dimethoxy-PEA
        44	2C-T-8	4-Cyclopropylmethylthio-2,5-dimethoxy-PEA
        45	2C-T-9	4-(t)-Butylthio-2,5-dimethoxy-PEA
        46	2C-T-13	4-(2-Methoxyethylthio)-2,5-dimethoxy-PEA
        47	2C-T-15	4-Cyclopropylthio-2,5-dimethoxy-PEA
        48	2C-T-17	4-(s)-Butylthio-2,5-dimethoxy-PEA
        49	2C-T-21	4-(2-Fluoroethylthio)-2,5-dimethoxy-PEA
        50	4-D	4-Trideuteromethyl-3,5-dimethoxy-PEA
        51	beta-D	beta,beta-Dideutero-3,4,5-trimethoxy-PEA
        52	DESOXY	4-Methyl-3,5-Dimethoxy-PEA
        53	2,4-DMA	2,4-Dimethoxy-A
        54	2,5-DMA	2,5-Dimethoxy-A
        55	3,4-DMA	3,4-Dimethoxy-A
        56	DMCPA	2-(2,5-Dimethoxy-4-methylphenyl)-cyclopropylamine
        57	DME	3,4-Dimethoxy-beta-hydroxy-PEA
        58	DMMDA	2,5-Dimethoxy-3,4-methylenedioxy-A
        59	DMMDA-2	2,3-Dimethoxy-4,5-methylenedioxy-A
        60	DMPEA	3,4-Dimethoxy-PEA
        61	DOAM	4-Amyl-2,5-dimethoxy-A
        62	DOB	4-Bromo-2,5-dimethoxy-A
        63	DOBU	4-Butyl-2,5-dimethoxy-A
        64	DOC	4-Chloro-2,5-dimethoxy-A
        65	DOEF	4-(2-Fluoroethyl)-2,5-dimethoxy-A
        66	DOET	4-Ethyl-2,5-dimethoxy-A
        67	DOI	4-Iodo-2,5-dimethoxy-A
        68	DOM (STP)	4-Methyl-2,5-dimethoxy-A
        69	Psi-DOM	4-Methyl-2,6-dimethoxy-A
        70	DON	4-Nitro-2,5-dimethoxy-A
        71	DOPR	4-Propyl-2,5-dimethoxy-A
        72	E	4-Ethoxy-3,5-dimethoxy-PEA
        73	EEE	2,4,5-Triethoxy-A
        74	EEM	2,4-Diethoxy-5-methoxy-A
        75	EME	2,5-Diethoxy-4-methoxy-A
        76	EMM	2-Ethoxy-4,5-dimethoxy-A
        77	ETHYL-J	N,alpha-diethyl-3,4-methylenedioxy-PEA
        78	ETHYL-K	N-Ethyl-alpha-propyl-3,4-methylenedioxy-PEA
        79	F-2	Benzofuran-2-methyl-5-methoxy-6-(2-aminopropane)
        80	F-22	Benzofuran-2,2-dimethyl-5-methoxy-6-(2-aminopropane)
        81	FLEA	N-Hydroxy-N-methyl-3,4-methylenedioxy-A
        82	G-3	3,4-Trimethylene-2,5-dimethoxy-A
        83	G-4	3,4-Tetramethylene-2,5-dimethoxy-A
        84	G-5	3,4-Norbornyl-2,5-dimethoxy-A
        85	GANESHA	3,4-Dimethyl-2,5-dimethoxy-A
        86	G-N	1,4-Dimethoxynaphthyl-2-isopropylamine
        87	HOT-2	2,5-Dimethoxy-N-hydroxy-4-ethylthio-PEA
        88	HOT-7	2,5-Dimethoxy-N-hydroxy-4-(n)-propylthio-PEA
        89	HOT-17	2,5-Dimethoxy-N-hydroxy-4-(s)-butylthio-PEA
        90	IDNNA	2,5-Dimethoxy-N,N-dimethyl-4-iodo-A
        91	IM	2,3,4-Trimethoxy-PEA
        92	IP	3,5-Dimethoxy-4-isopropoxy-PEA
        93	IRIS	5-Ethoxy-2-methoxy-4-methyl-A
        94	J	alpha-Ethyl-3,4-methylenedioxy-PEA
        95	LOPHOPHINE	3-Methoxy-4,5-methylenedioxy-PEA
        96	M	3,4,5-Trimethoxy-PEA
        97	4-MA (PMA)	4-Methoxy-A
        98	MADAM-6	2,N-Dimethyl-4,5-methylenedioxy-A
        99	MAL	3,5-Dimethoxy-4-methallyloxy-PEA
        100	MDA	3,4-Methylenedioxy-A
        101	MDAL	N-Allyl-3,4-methylenedioxy-A
        102	MDBU	N-Butyl-3,4-methylenedioxy-A
        103	MDBZ	N-Benzyl-3,4-methylenedioxy-A
        104	MDCPM	N-Cyclopropylmethyl-3,4-methylenedioxy-A
        105	MDDM	N,N-Dimethyl-3,4-methylenedioxy-A
        106	MDE	N-Ethyl-3,4-methylenedioxy-A
        107	MDHOET	N-(2-Hydroxyethyl)-3,4-methylenedioxy-A
        108	MDIP	N-Isopropyl-3,4-methylenedioxy-A
        109	MDMA	N-Methyl-3,4-methylenedioxy-A
        110	MDMC (Methylone)	N-Methyl-3,4-ethylenedioxy-A
        111	MDMEO	N-Methoxy-3,4-methylenedioxy-A
        112	MDMEOET	N-(2-Methoxyethyl)-3,4-methylenedioxy-A
        113	MDMP	alpha,alpha,N-Trimethyl-3,4-methylenedioxy-PEA
        114	MDOH	N-Hydroxy-3,4-methylenedioxy-A
        115	MDPEA	3,4-Methylenedioxy-PEA
        116	MDPH	alpha,alpha-Dimethyl-3,4-methylenedioxy-PEA
        117	MDPL	N-Propargyl-3,4-methylenedioxy-A
        118	MDPR	N-Propyl-3,4-methylenedioxy-A
        119	ME	3,4-Dimethoxy-5-ethoxy-PEA
        120	MEDA	3-methoxy-4,5-Ethylenedioxy-A [Erowid corrected]
        121	MEE	2-Methoxy-4,5-diethoxy-A
        122	MEM	2,5-Dimethoxy-4-ethoxy-A
        123	MEPEA	3-Methoxy-4-ethoxy-PEA
        124	Meta-DOB	5-Bromo-2,4-dimethoxy-A
        125	Meta-DOT	5-Methylthio-2,4-dimethoxy-A
        126	Methyl-DMA	N-Methyl-2,5-dimethoxy-A
        127	Methyl-DOB	4-Bromo-2,5-dimethoxy-N-methyl-A
        128	Methyl-J	N-Methyl-alpha-ethyl-3,4-methylenedioxy-PEA
        129	Methyl-K	N-Methyl-alpha-propyl-3,4-methylenedioxy-PEA
        130	Methyl-MA	N-Methyl-4-methoxy-A
        131	Methyl-MMDA-2	N-Methyl-2-methoxy-4,5-methylenedioxy-A
        132	MMDA	3-Methoxy-4,5-methylenedioxy-A
        133	MMDA-2	2-Methoxy-4,5-methylenedioxy-A
        134	MMDA-3a	2-Methoxy-3,4-methylenedioxy-A
        135	MMDA-3b	4-Methoxy-2,3-methylenedioxy-A
        136	MME	2,4-Dimethoxy-5-ethoxy-A
        137	MP	3,4-Dimethoxy-5-propoxy-PEA
        138	MPM	2,5-Dimethoxy-4-propoxy-A
        139	Ortho-DOT	2-Methylthio-4,5-dimethoxy-A
        140	P	3,5-Dimethoxy-4-propoxy-PEA
        141	PE	3,5-Dimethoxy-4-phenethyloxy-PEA
        142	PEA	PEA
        143	PROPYNYL	4-Propynyloxy-3,5-dimethoxy-PEA
        144	SB	3,5-Diethoxy-4-methoxy-PEA
        145	TA	2,3,4,5-Tetramethoxy-A
        146	3-TASB	4-Ethoxy-3-ethylthio-5-methoxy-PEA
        147	4-TASB	3-Ethoxy-4-ethylthio-5-methoxy-PEA
        148	5-TASB	3,4-Diethoxy-5-methylthio-PEA
        149	TB	4-Thiobutoxy-3,5-dimethoxy-PEA
        150	3-TE	4-Ethoxy-5-methoxy-3-methylthio-PEA
        151	4-TE	3,5-Dimethoxy-4-ethylthio-PEA
        152	2-TIM	2-Methylthio-3,4-dimethoxy-PEA
        153	3-TIM	3-Methylthio-2,4-dimethoxy-PEA
        154	4-TIM	4-Methylthio-2,3-dimethoxy-PEA
        155	3-TM	3-Methylthio-4,5-dimethoxy-PEA
        156	4-TM	4-Methylthio-3,5-dimethoxy-PEA
        157	TMA	3,4,5-Trimethoxy-A
        158	TMA-2	2,4,5-Trimethoxy-A
        159	TMA-3	2,3,4-Trimethoxy-A
        160	TMA-4	2,3,5-Trimethoxy-A
        161	TMA-5	2,3,6-Trimethoxy-A
        162	TMA-6	2,4,6-Trimethoxy-A
        163	3-TME	4,5-Dimethoxy-3-ethylthio-PEA
        164	4-TME	3-Ethoxy-5-methoxy-4-methylthio-PEA
        165	5-TME	3-Ethoxy-4-methoxy-5-methylthio-PEA
        166	2T-MMDA-3a	2-Methylthio-3,4-methylenedioxy-A
        167	4T-MMDA-2	4,5-Thiomethyleneoxy-2-methoxy-A
        168	TMPEA	2,4,5-Trimethoxy-PEA
        169	2-TOET	4-Ethyl-5-methoxy-2-methylthio-A
        170	5-TOET	4-Ethyl-2-methoxy-5-methylthio-A
        171	2-TOM	5-Methoxy-4-methyl-2-methylthio-A
        172	5-TOM	2-Methoxy-4-methyl-5-methylthio-A
        173	TOMSO	2-Methoxy-4-methyl-5-methylsulfinyl-A
        174	TP	4-Propylthio-3,5-dimethoxy-PEA
        175	TRIS	3,4,5-Triethoxy-PEA
        176	3-TSB	3-Ethoxy-5-ethylthio-4-methoxy-PEA
        177	4-TSB	3,5-Diethoxy-4-methylthio-PEA
        178	3-T-TRIS	4,5-Diethoxy-3-ethylthio-PEA
        179	4-T-TRIS	3,5-Diethoxy-4-ethylthio-PEA
        }

        return smiles