--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2
-- Dumped by pg_dump version 16.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: logins; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.logins (id, username, password_hash, role, created_at, session_token) FROM stdin;
3a774d44-e014-413a-9d9b-6a60a81d2448	admin	scrypt:32768:8:1$D3EsmbzGGN3e9yuJ$d077623c04561ad8f0721655c4d0e61751ec5464ef89f71365ccedc5280cd0b5973124313d22dd3bbb19701c76501f093bf285c615ea4f12f5a268b176449d61	admin	2025-12-11 23:31:11.932626	bb497580-0d3a-4ee2-9846-45bb544697a4
fd659845-6571-4b19-b8e1-1cba0ff0b60b	Test Mining Company	scrypt:32768:8:1$HE9lC18QYtHUNS7R$602195e92f60bef235bdef922eed06f6d878f9ba80c92d1e5a29bbf393dccd86560c8820ad3a169d39615a6660561a3b58ce1127e0a4da90bd1b38d0547af511	company	2025-12-13 05:57:05.232052	3f796316-052e-4223-84c9-effff64866fd
4bb8fc65-f6ca-4f40-9638-167c6f253780	deltafive	scrypt:32768:8:1$4rWPRbSQpFoXOE3g$37cd8ef97eebd56cbe53da1a6ded0b0b1fa2a69b4f21aff29b17889e75f1ee535dae544ada3c3b55d044ff1afa1411ae377e06088143123e6a433d1ba446af78	company	2025-12-13 06:04:04.610991	afd4e286-dc45-4c89-99bc-9f21dc14829a
fed24040-96ff-4da0-8ae8-a371e4fd136e	quality	scrypt:32768:8:1$NEhfCTxmCbO8djOI$3079544d67857fcbb07d6de710ef97e7675edd465f0d82dfb770244e696bbcb0f66a1fc86ae9f6445d1a0e098b318d105258b2f953ddbce205749f88606a2acd	company	2025-12-13 08:36:19.114316	6c3dbe40-9a61-4f39-94ca-0c8e4e8cc172
2a7cc0b4-97c5-433b-ac92-45ad011c8dac	axiscet	scrypt:32768:8:1$NOo2x2Cu58cLv7Eb$44e4ebe53a94d4d3464b9cd1ff9ab508545104691b656fd612fc38060d2240a61b45bd529a8f8b3ffecf666c475383cd2a0404cd1158e010ac08aebb7bee5949	college	2025-12-13 09:36:29.190267	8a16bf5c-538d-473b-89b4-3da28b91d21d
9afa7c4d-fca1-4b0b-8312-df94187bbeb3	tcstvm	scrypt:32768:8:1$UzXHjl7FbJ2bqmuX$47668cac71a11cfe5363910b7ed0fd325d62c983881a0ce76c52936c98da2031fb2584321268bafdf287d4649e842d2ac526724da639fccca476ab756a96063b	company	2025-12-18 09:00:56.458718	261b7596-aac5-4f5b-a108-d6dde2a064e5
b2979fe8-89de-4042-aff9-a35d9d926887	uberindia	scrypt:32768:8:1$f4hCkMkZQyWVs6jL$d297e4a740ebb2b32e8357941defabd06699273a074e8508a8a855c552a153afafecac7ca648066c9be7f2c0f4012897803495db39471381f5ca83172ab85661	company	2025-12-13 09:55:17.287325	0d56dc07-3a42-4423-b979-ab8667ea7d1a
d9ef5bd4-0b7f-4591-8cd6-02e8f7e9f117	lbstvm	scrypt:32768:8:1$6FezFfx4PSMPH6go$fc5d09d757881e56594905f63d6555d41bcd67b90643cf93c035bd39de64dbfe09c8f38eb5ef96cf438f93d24c972c940361da5862b80c243dcfd45b08a63754	college	2025-12-18 07:55:32.311197	f99d041c-bfc9-4c85-8bb2-3151969e3d75
2eefce16-0738-4410-a9f9-a72e358ed939	christtvm	scrypt:32768:8:1$eataHMcjgFzU372z$7f73e6fdecd30e110af49e223f2962cad31efa01b995f7197495455757226e68f73c44ab39083733766ae33dd197e25a46531135490ea9e238c635dbb170aceb	college	2025-12-18 07:57:05.984292	b1b60e0b-97ff-4986-836f-d1e0adaa4388
aee8b47c-c198-4bd8-8782-b5cecd6c3349	rajagiri	scrypt:32768:8:1$T2a9RpC1n2XcPUgk$7ec907e690b52a961911d2ba466203062b36ac681e0b6dc66b7405d9da9e1c6b852f50047c5d6f654ec8efa1cc22fe858fb0a8357241641bd93e994c01ea4c64	college	2025-12-18 07:58:05.136613	ccd5ec0d-6280-488f-a213-9d0e94cd9922
67ec34eb-ea24-46b9-bcad-12dcb4f43499	pits	scrypt:32768:8:1$UsEEU1sgPajwQLn9$248bf443afb416983be7b19d28e00e5d9d570e760699af6a22bfc61237aa7ef8bce3a319a3720518db32e506ca3de1ef0d3d3d6d1cdee9aee08215eb425108af	company	2025-12-18 09:01:20.512253	0fd6035a-4ead-4d6b-b83f-6d53ec333d19
e5fbac8f-84a1-4b99-82d6-bfecbcc4f58b	4hrslab	scrypt:32768:8:1$za9qJTtw2vakLsqw$19aae6d9f2c167bcd871f49210f7cbc1d3ad83eae5c39a9e6cfd5cb5bb6292b2e574d05dab00e8589a835383137e991529c9a4c905420f7203f7a14cb968a6ee	company	2025-12-18 09:04:41.461453	d9e7827a-5afe-4f04-bc13-728aff9d6942
177cb994-d8dc-4b1d-9a0c-2f3c91dcceef	testcompany1	scrypt:32768:8:1$9ihHuWcehY37d20W$9628d61524ad6012282585cb89cf03577cba0d2a3a15ebd0c946528bcddb803c415bf5e435185df88bfdd375c66c1f359d7bb5e4137d40f4cb5dc88ee9458652	company	2025-12-18 09:05:35.097448	16005d7d-481c-4ad1-be95-9ca9d507cf61
25f25162-4873-4810-9e64-c41f538f2a9f	testcompany2	scrypt:32768:8:1$V7hz2Q1aBigc0FnX$b1b2124ce9734e73bb0f5b0e9666fff6fb74d2b2d403e757c26fe7937b3e6c8d6893cc4bbc09b5f855851a46ab18c1892b2ada49fccf80a095fc892b3eab12c0	company	2025-12-18 09:05:53.879326	d92180af-dc30-42b0-a954-f75bf1883ec9
007096c9-d8b4-4762-9fdf-969d1d217442	testcompany3	scrypt:32768:8:1$pfAVtNjOd4MRfliW$a61d290d4af894ed77a750ae6634e2fafa1ee2fad5f1c05dddfd10c2940bb503c815a718ae2c2d86102338236f7b5267fd911dc9b9af40733c9a9bd23f6e89eb	company	2025-12-18 09:06:19.85782	5f279e84-5703-4df8-b54b-77278aef4736
d3409299-4890-4a89-8896-ea4e89ecf851	testcompany4	scrypt:32768:8:1$hkzt1s6H6gkx3KzQ$81cfd81b06024aa220c1584caebd77cd4bed5f50858a1e613006803431894a50832e9e24335eb3285fca381ced84da6ebbc9fbd460c06d37d4512c6c48d7babf	company	2025-12-18 09:06:39.296065	5c9d00e9-5e91-44bd-9a15-9514dc612a26
cdb2ac1b-494a-433d-9370-9206ee1b5690	testcompany6	scrypt:32768:8:1$64RwcLnlvokCcE0x$6745b592d92cb03bf470b498f214f116cd4f902c0a454228bba1d309769cb75d522da89e674d87320fabb0d2817cab17f97d5412cb01d069c729832c2d8529d3	company	2025-12-18 09:07:04.000614	800d4a45-6b51-49f4-acb3-76b85e7e5062
b39c1cb1-1269-40e9-a3b0-d962e6599357	testcompany7	scrypt:32768:8:1$2CqEtv9AEnxHNZbx$f0a1b493c359e959d424fa79df12fb3f7736368e2c3cb99ea1c2901f25e17a27e08767a4b967c10d044e73bbdd2c316840b4760ee70d6e8a46101a1e38b6798a	company	2025-12-18 09:08:24.935902	6053a287-f1a7-4462-8fe8-b8a5e28e74e4
5f9f866b-374d-49a9-ab6e-a6a1d21d44e6	VR Tech Solutions	scrypt:32768:8:1$kXSNitAuPTxXEpYo$0df648ee67c77188d51956ed81a1e41abf5b51cdb8de59d2f413de5000c057e2303eaf95ffc90face82534f41f803e6349d0d1882c1ee7328e649a84914be6d3	company	2025-12-18 16:21:30.217171	d411a074-ab06-4d87-90fe-15675c7f689c
d8d64784-6edf-4b70-bad3-3d8cc54bd270	24gear	scrypt:32768:8:1$kVvaVfS99vKeR0lu$ad85a0d794e2b1659bac703ee5b5511cfb2e3f2f0b95840dba041f4357f0af33710770c507e46b1131e4a8f1edf254225c19ac55f058c2f4f91d00641dc7c158	company	2025-12-27 05:22:31.76716	6c33b65a-72ce-4357-b29a-f395730ccc7d
b218045a-54f2-473f-a895-8f10b1a17026	22gear	scrypt:32768:8:1$HW4Ec2QqOdZcDiwo$97d895811d8cce0a84ef175984c9892f12a5b1e1608b85941297e4b530fc7b88effd75d826c855ca240e06266dac7ca44996cc60ce06766c9019f4f39c0663b1	company	2025-12-27 05:34:42.736076	e4ac3eef-2633-4917-aa0f-463a7598f5b7
01b9049a-78d7-4dab-a398-4c4c6ab2412c	222	scrypt:32768:8:1$P99geEt5w2LRi7nS$7b3330eaf64545ab10ef18cef15d88772657f82db9937ba33c7df786a80fbe5ae3fe4058c372fbcc1bc058f77c0f60f9da1b440369af885be70f4456e2f4ad5d	company	2025-12-27 05:36:55.815559	059b99cf-3f8a-4b85-b0b7-90643339259a
a8328144-b540-4dbc-a3e5-705a7913cff7	InternationalConglomerateLtd	scrypt:32768:8:1$5Ou7ssxbOcfMtIjK$04e40f7ef81be206cbf751af2fd3766f15604843a4ca31af8c3e0f679dc927c8f8029b214595951c991c96df7480485cd191e2c2360a90690e58bd9ea8ee08fe	company	2025-12-27 05:43:41.417073	b90a3926-31ae-4727-b0f9-49449cee277b
59344b9e-546f-4758-895f-f54195da6d02	vrtech	scrypt:32768:8:1$iHkiG4pMflhbGoiI$ad3b6478da6491ac19443108cd47e43db3791e18e4d973a48541f2be418c417b06b845ada5e9fe86edca7ce675178128c90300e727e2a8a698ef6c5d88880e81	company	2025-12-27 06:05:57.271666	4305ca82-35c0-4fb9-9bc5-ef6eb2935c83
e6038c34-e922-41df-9aaf-e035f80601e1	sinoj	scrypt:32768:8:1$VKOhAf5zCT2Wp3gf$9dd97358e81fc6088f0efb7b209864d25bf4276ec3ea230ed06b1476bc7dad1a061f0606cffe14a537f3ed54b205752c5da9e629fe3dba5c827d947426d3d110	user	2025-12-27 07:42:21.317531	37e1d17d-3817-4150-9488-6688b8b52a81
243475a3-0369-4287-b755-e85fb93cd1f4	jeethu	scrypt:32768:8:1$1zyNCUC3rQs4NTiy$b27d5dd828f70b9660769273b7f48e2bd8ff2d85c03bd65c20e7ac0eb77e29da98ec5fce97b844b051da08dfa14b9f0553704d7b8a47ea9dd95aac46563616c0	user	2025-12-27 07:42:40.089551	ee084b20-cacb-4584-8564-a725db705592
2032cdad-7746-4d7a-ad20-87a8a9b00fcd	aparna	scrypt:32768:8:1$cjTla5fwaIyHw3RJ$532b4cb1742412418b6f4dea20e823e550462710756b92386168dd012644837fc481d019d4815ddd9240c7e83537fa787abba5753f48af59df292f787b919bdc	user	2025-12-27 07:43:07.201378	013d8f74-bf70-48a3-8643-a5361db92647
17bdd5c4-e1e4-4ef7-bb56-971d0454b3f2	arun	scrypt:32768:8:1$eGI943sRdJrq2s10$f6f6cbc8fcd37e3376230090761846a87463eb514bb3b51e39516f11e41b915d3db46ae3f27ff47c8d40f986b70e63d399c409d08f34211d244a7dfb92302fd5	user	2025-12-27 07:43:56.877766	738dfe82-26cf-45de-a184-f703005047e3
8c516af1-7abd-4a32-9981-e16191503a12	omprakash	scrypt:32768:8:1$pQNsEHwHMAGJj7Tf$afd14b0aa5dfb885812db258b5af52d587091f34701af1f42b1a1d805ef7e9983c98c32711725761fab87122b8f979389eaaaff2a3842bfde36579cd03509a9a	user	2025-12-27 07:44:24.915917	56112745-6fad-40f3-a4b2-7b7342416225
a958e670-4c7f-47cf-a375-7d8ea656c009	anju	scrypt:32768:8:1$LklzCltKvuxENgiQ$dccdcd467e750f8f9c62eaaace575f44e0715f7657879a04c0c0fb098e3cafb0d0716a9e86922425986b86da21a282eea188a09616764644049d0550bbf51998	user	2025-12-27 07:44:44.677315	93662b95-5ea7-4e60-a490-4971132776dd
d705b877-1c1e-41fb-813d-7ecc681575e7	akhila	scrypt:32768:8:1$uEgkO6wUx9IfjgVM$00377b89bd12b93a22337123de6238d440ffe0bb20bab420877f012a3c33dbe7ecf3fcc2159f60d0714048a1626d805f5145261ae124a1392f7e533ff06ab89e	user	2025-12-27 07:45:12.225782	27fbe949-ad76-49d1-8c5e-6342de46cfd4
43bb11dc-7faa-4259-9e75-071438d190ca	rajesh	scrypt:32768:8:1$6H9tKnNS1tRj19av$249b807f4f19977d2d9c8fc835ab615a03bd4924a8f0d934286954469b67951bb908f9d58ae02bd0a509c3e3399f3420357e342d3b36891d865faf3f4f7746ba	user	2025-12-27 07:45:35.997464	2d58fd18-750b-42b3-9856-eb5201f4e524
5efc0cf9-6658-42fa-9122-129640ee915f	ziyad	scrypt:32768:8:1$e3pSHqBOGX9iksAt$95dd407b91dba081b5050d0454bfb04a4f248e85b15d5d563bbb7f76d4aff56895e13821e3fd5eaf818e673172c181139f7dab5e05297fcc1ae63bccbf556468	user	2025-12-27 07:46:00.020793	66938755-3d3b-4a35-8237-d7befa19d596
e50182b3-507d-49f2-802c-807f80ac61a9	sudarshan	scrypt:32768:8:1$Y4IxIJ0SElVqP1j9$ec5b72f405f2495075545b0069440627dc9f5e66a3fad233bef4cf9eb3f12cb7c6613ac3fccc1ed4d2e8a6bf3579740512ad4382b29b8dd793645f3cb04dda7b	user	2025-12-27 07:47:13.701308	80bcbad7-ed8b-4fb5-b4a1-8c530949e1ee
40ad8898-4729-495c-a473-4d88662d112a	pawan	scrypt:32768:8:1$aIXtAFkP8mnjouJB$08eec32bb7573c7d27a9c5d2240456d66b05d3b9278dbbff34f6a8c6ca02529f9c475593517f22116306c345e3aebd1a99a050f86c4c530f6be1c2fa13165f1c	user	2025-12-27 07:47:45.086283	d6d3140c-f01a-483f-b67b-59c5e90c7d6b
16399907-e0eb-429c-98f9-8159a1ba4fd0	aman	scrypt:32768:8:1$V6vicj3iH14C4gIy$535e3a23d1bd07a50b4e251fb9facef1935587797346124e736f6a7c4d14e2acd93c3604b4c11eebf451e318089607f1b94c77ae3b6bcb3348957311c57fdc6a	user	2025-12-27 07:48:03.536	5c881d92-9cfd-4fe5-8112-baff1ea71eb4
b401fea4-f334-45a6-9e5b-e8f205b27afa	newguest	scrypt:32768:8:1$TpDOMasacHuweHvD$1b8bad6cc5fddc8e7af7648c20eaafb174cfa34b7bdfa56370c5d230d68e12ab19099240cf7e838ee7217c4a165a5c70dff263399c5bc138af8ad0d1bc0c0761	user	2025-12-27 07:52:18.112677	8f050d6e-a317-4932-bc9c-37ea2f3ca1f8
698c652d-1371-4e0f-9bb7-1a391f6210a3	kavya	scrypt:32768:8:1$QgWXgLzT7FboM0wp$be667ad18dabc7e5a9a8b7a4f160a8ea2ad1c7053a30e01a21f1cf992b244948190059b09665f2794a386560be6b1deb29dd94e0e9858e528075059d6e4f1364	user	2025-12-27 08:20:36.307695	279dc9a0-2367-46a4-9dc8-8bac03cc62ca
c873eef6-a5e4-40f7-abe7-844962d69b08	sasta	scrypt:32768:8:1$KpxWQclWM9z6yqjc$d6c99aabede04f5d550ac3c56f6782af34422328f39dc8b06930f85f3c925fa31cbbf77fbac478ec1b08d181c7e86557867a620b8f9e1d9858aeb40fa0b4d6ec	company	2025-12-27 09:06:39.282364	970f538f-1820-4c0a-b93d-95eea62c894c
3b7ce9fc-8d47-41c8-9c03-61ef7f1f668c	quest	scrypt:32768:8:1$lZ0ZFJAZcWjH0C2H$41b30b28220456d045c9c2918d95ceeae5f3e8b277023c9ce84a72f3e06e16f37aae96fd72e60b039d93564303c323f64057e98ad1fe0ae7971102bfdf3f009a	company	2025-12-27 17:16:03.785326	7fcb2997-1950-419b-84fc-176a56aea781
\.


--
-- Data for Name: admins; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.admins (id, login_id, name, email, created_at, updated_at) FROM stdin;
1ce0fee0-ff9f-44b6-8d14-3fa9930e915c	3a774d44-e014-413a-9d9b-6a60a81d2448	admin	admin@g.com	2025-12-11 23:31:11.93648	2025-12-11 23:31:11.936488
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, login_id, name, email, phone, age, about_me, profile_picture, created_at, college_name, is_banned, updated_at) FROM stdin;
1f3247f5-e9d8-49d6-870c-dab899925124	17bdd5c4-e1e4-4ef7-bb56-971d0454b3f2	arun	arun@gmail.com	\N	\N	\N	\N	2025-12-27 07:43:56.878732	Rajagiri College	f	2025-12-27 09:21:23.471116
ecca8cf1-635b-4d81-8113-cb21f666e1b4	d705b877-1c1e-41fb-813d-7ecc681575e7	akhila	akhila@gmail.com	\N	\N	\N	\N	2025-12-27 07:45:12.226913	Rajagiri College	f	2025-12-27 09:51:30.455506
82c879bd-3a41-4703-bbb9-b5f2f386405d	e6038c34-e922-41df-9aaf-e035f80601e1	SINOJ GEORGE	sinojgeorge@example.com	9876543210	26	Master of Computer Applications (MCA) graduate from Kerala University (2024 batch) with First Class distinction. My academic journey focused on advanced topics: Distributed Systems, Machine Learning, Cybersecurity, and Cloud Computing. Final year project: "Smart Healthcare Monitoring System using IoT and ML" awarded 'Best Project' at university level.\r\n\r\nTechnical Skills: \r\n• Programming: Java (Spring Boot), Python (Django), JavaScript (React/Node.js)\r\n• Databases: MySQL, MongoDB, PostgreSQL\r\n• DevOps: Docker, AWS EC2, Git, CI/CD\r\n• Tools: Postman, Jira, VS Code, Eclipse\r\n\r\nCompleted 6-month internship at FinTech Corp where I contributed to microservices architecture implementation. Active participant in coding competitions (CodeChef 3-star). Strong problem-solving abilities with 300+ problems solved on LeetCode. Looking for software development roles to build scalable solutions and learn industry best practices.\r\n\r\nCareer Objective: Seeking challenging software engineering positions where I can contribute to innovative projects, collaborate with experienced teams, and continuously enhance my technical expertise while delivering value to the organization.	\N	2025-12-27 07:42:21.31948	christtvm	f	2025-12-27 09:10:21.946994
893b67a5-be80-42da-bb74-f0a4345976e7	243475a3-0369-4287-b755-e85fb93cd1f4	jeethu	jeethu@gmail.com	\N	\N	\N	\N	2025-12-27 07:42:40.090825	Rajagiri College	f	2025-12-27 09:53:23.824302
33ab1367-1d38-4707-b2b1-5701dfd4c382	2032cdad-7746-4d7a-ad20-87a8a9b00fcd	Aparna Asok	aparnaasok@gmail.com	\N	\N	\N	\N	2025-12-27 07:43:07.202479	Rajagiri College	f	2025-12-28 05:46:26.616058
f4d4e565-1774-4b99-b4c3-541cd6946b9f	698c652d-1371-4e0f-9bb7-1a391f6210a3	kavya	kavya@gmail.com	\N	\N	\N	\N	2025-12-27 08:20:36.308975	Rajagiri College	f	2025-12-28 06:48:58.006892
f076030b-e082-4dba-a866-e6a31f41416b	40ad8898-4729-495c-a473-4d88662d112a	pawan	pawan@gmail.com	\N	\N	\N	\N	2025-12-27 07:47:45.087304	Christ College	f	2025-12-28 07:36:46.354784
f2aeb083-c9d4-44bb-ab81-e2239b0f9074	8c516af1-7abd-4a32-9981-e16191503a12	omprakash	omprakash@example.com	\N	\N	\N	\N	2025-12-27 07:44:24.918502	\N	f	2025-12-27 07:44:24.918507
7f796137-e8fb-4665-acdb-bee49bee518a	a958e670-4c7f-47cf-a375-7d8ea656c009	anju	anju@gmail.com	\N	\N	\N	\N	2025-12-27 07:44:44.678777	\N	f	2025-12-27 07:44:44.678781
579eef83-2871-47f1-ae50-acdf21121555	43bb11dc-7faa-4259-9e75-071438d190ca	rajesh	rajesh@gmail.com	\N	\N	\N	\N	2025-12-27 07:45:35.998378	\N	f	2025-12-27 07:45:35.998382
d12b7e25-659d-4e8e-816d-307a6eebda2a	5efc0cf9-6658-42fa-9122-129640ee915f	ziyad	ziyad@yahoo.co.in	\N	\N	\N	\N	2025-12-27 07:46:00.022421	\N	f	2025-12-27 07:46:00.022426
f0f58766-844d-4da1-a346-b7275937e53c	e50182b3-507d-49f2-802c-807f80ac61a9	sudarshan	sudarshan@example.com	\N	\N	\N	\N	2025-12-27 07:47:13.70232	\N	f	2025-12-27 07:47:13.702323
01166ff5-cf0b-4c54-a384-6aa006ce7fc7	16399907-e0eb-429c-98f9-8159a1ba4fd0	aman	aman@gmail.com	\N	\N	\N	\N	2025-12-27 07:48:03.537031	\N	t	2025-12-28 08:01:06.944375
a26e4670-b881-42cc-a7c5-2039d004a112	b401fea4-f334-45a6-9e5b-e8f205b27afa	newguest	newguest@example.com	\N	\N	\N	\N	2025-12-27 07:52:18.113929	\N	f	2025-12-28 08:05:34.209812
\.


--
-- Data for Name: resume_certifications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.resume_certifications (id, user_id, resume_path, uploaded_at) FROM stdin;
4392f776-230e-420c-9716-07c4478993e8	82c879bd-3a41-4703-bbb9-b5f2f386405d	static/uploads/resume_SINOJ GEORGE_resume.pdf	2025-12-27 15:14:00.613183
7bfaf903-3474-4449-bb4d-ff03e7241a4c	1f3247f5-e9d8-49d6-870c-dab899925124	static/uploads/resume_arun_sample10page.pdf	2025-12-27 15:17:41.920595
5a82565a-4fe2-47d5-8a84-488ad263e6d2	33ab1367-1d38-4707-b2b1-5701dfd4c382	static/uploads/resume_Aparna Asok_1pagepdf.pdf	2025-12-27 15:28:17.913928
b484da14-7356-4e00-abf5-c3e48336d689	01166ff5-cf0b-4c54-a384-6aa006ce7fc7	static/uploads/resume_aman_1page_doc.docx	2025-12-27 22:37:20.079215
caea90dd-37c1-4285-81ca-e9cf20cf1071	f4d4e565-1774-4b99-b4c3-541cd6946b9f	static/uploads/resume_kavya_sample10page.pdf	2025-12-28 12:20:56.132205
\.


--
-- Data for Name: certifications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.certifications (id, user_id, resume_cert_id, certification_name, verification_status, uploaded_at) FROM stdin;
d907179f-2c05-4fea-aea0-15568b49bfdc	82c879bd-3a41-4703-bbb9-b5f2f386405d	\N	Java	f	2025-12-27 15:14:27.567493
3e3a24e3-1454-40e0-bf1c-e4e4537f75a6	82c879bd-3a41-4703-bbb9-b5f2f386405d	\N	C++	f	2025-12-27 15:14:47.491021
5b171b41-d177-4891-855f-12916809bb41	1f3247f5-e9d8-49d6-870c-dab899925124	\N	Excel	t	2025-12-27 15:16:14.107596
29b9c231-f74c-43df-91eb-57d32e29c9a8	33ab1367-1d38-4707-b2b1-5701dfd4c382	\N	PHP, JAVA	f	2025-12-27 15:28:33.045366
c3f99ba1-cc8e-44e5-8551-c0e69cb5c5f6	01166ff5-cf0b-4c54-a384-6aa006ce7fc7	\N	Java	f	2025-12-27 22:37:25.741524
22fc9b96-ae5b-4947-a673-176265a14700	01166ff5-cf0b-4c54-a384-6aa006ce7fc7	\N	Spring Boot	f	2025-12-27 22:37:32.692332
1372d738-3395-42b8-a536-fc06403659d6	01166ff5-cf0b-4c54-a384-6aa006ce7fc7	\N	Oracle	f	2025-12-27 22:37:41.871595
12b4b6b9-37a0-4a36-a032-26983e55448a	33ab1367-1d38-4707-b2b1-5701dfd4c382	\N	PHP	t	2025-12-27 15:28:25.386859
7dac88b0-7433-411f-9bf4-41466a4a148c	f4d4e565-1774-4b99-b4c3-541cd6946b9f	\N	SQL	f	2025-12-28 12:20:29.286908
16dd6e72-878e-4705-831e-28d6912dcf2f	f4d4e565-1774-4b99-b4c3-541cd6946b9f	\N	Angular	t	2025-12-28 12:20:20.540924
\.


--
-- Data for Name: college; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.college (id, login_id, college_name, email, address, website, logo, description, is_banned, created_at, updated_at) FROM stdin;
eb49ce1e-c32a-4882-bc26-02d358aa6316	2a7cc0b4-97c5-433b-ac92-45ad011c8dac	AXIS College of Engineering & Technology	axiscet@gmail.com					f	2025-12-13 09:36:29.198229	2025-12-18 17:26:20.99644
dd5c0787-62e7-4baf-b637-3c1b16d86a45	d9ef5bd4-0b7f-4591-8cd6-02e8f7e9f117	LBS trivandrum	lbstvm@gmail.com					f	2025-12-18 07:55:32.31339	2025-12-18 18:09:05.47668
eb293b68-595b-4d67-9b19-45c5ad8a3f44	2eefce16-0738-4410-a9f9-a72e358ed939	Christ College	christtvm@yahoo.co.in	Trivandrum				f	2025-12-18 07:57:05.990207	2025-12-27 09:10:50.455174
e801184a-e874-4467-9d13-042701aacd1b	aee8b47c-c198-4bd8-8782-b5cecd6c3349	Rajagiri College	admin@rajagiri.edu	Kochi				f	2025-12-18 07:58:05.138837	2025-12-27 09:17:40.394195
\.


--
-- Data for Name: companies; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.companies (id, login_id, company_name, email, address, website, logo, description, industry, is_banned, created_at, updated_at) FROM stdin;
de9360fc-8a2d-46d2-b17b-3374664ba2b9	fd659845-6571-4b19-b8e1-1cba0ff0b60b	Test Mining Company	testminingcompany@gmail.com	Sector A\nMain Road Collectorate\nJharkhand		https://drive.google.com/file/d/1gXfJpwyBn3eVfmyr5XGXf9KpjBnjwCMn/view?usp=drive_link	We focus on extracting key minerals (coal, iron ore, diamonds, limestone, etc.) for industrial growth, using mechanization, technology, and increasing sustainability efforts, contributing significantly to India's economy while engaging in exploration, large-scale operations, and community development	Mining and Quarrying	f	2025-12-13 05:57:05.243343	2025-12-13 05:57:05.243348
358c12e8-c9f7-4927-9719-19a23ebc40e4	b2979fe8-89de-4042-aff9-a35d9d926887	Uber India	uberindia@gmail.com					Accommodation and Food Service Activities	f	2025-12-13 09:55:17.289059	2025-12-28 05:49:01.182466
3275c0a0-5fcb-48c8-b6af-8e35fefc57ae	4bb8fc65-f6ca-4f40-9638-167c6f253780	delta5	delta5@example.com	Plot No 69-B,C,D, \r\nBommasandra Industrial Area, \r\nHosur Main Road, \r\nBangalore, \r\nKarnataka, \r\nPIN-560099.			Delta Five Systems was founded in 2014 with a belief that advanced technology, artificial intelligence and robotics could help improve the guest experience properly	Information and Communication	f	2025-12-13 06:04:04.612785	2025-12-13 07:49:27.232233
5543614c-7640-4723-b2a9-91cd648505e3	67ec34eb-ea24-46b9-bcad-12dcb4f43499	pits	pitstvm@gmail.com	\N	\N	\N	\N	\N	f	2025-12-18 09:01:20.513394	2025-12-18 09:01:20.513397
40fff6e1-df87-4b69-afa5-a041afda0be1	e5fbac8f-84a1-4b99-82d6-bfecbcc4f58b	4hrslab	labtvm@gmail.com	\N	\N	\N	\N	\N	f	2025-12-18 09:04:41.462585	2025-12-18 09:04:41.462588
317448de-a968-49bf-8e6a-6a8d3c89db1d	177cb994-d8dc-4b1d-9a0c-2f3c91dcceef	testcompany1	testcompany12@otmail.com	\N	\N	\N	\N	\N	f	2025-12-18 09:05:35.09847	2025-12-18 09:05:35.098473
03870015-093c-4077-911d-504f82bd2f01	25f25162-4873-4810-9e64-c41f538f2a9f	testcompany2	testcompany2@gmail.com	\N	\N	\N	\N	\N	f	2025-12-18 09:05:53.880257	2025-12-18 09:05:53.88026
ef007c8b-dde8-4c1e-b259-72c7724941da	007096c9-d8b4-4762-9fdf-969d1d217442	testcompany3	testcompany3@gmail.com	\N	\N	\N	\N	\N	f	2025-12-18 09:06:19.85882	2025-12-18 09:06:19.858824
6a4add7b-f2cc-4e6b-aa32-7ebfcc5e2985	d3409299-4890-4a89-8896-ea4e89ecf851	testcompany4	testcompany4@gmail.com	\N	\N	\N	\N	\N	f	2025-12-18 09:06:39.297547	2025-12-18 09:06:39.297553
992c5679-1ae1-4819-b0bb-088617998f40	cdb2ac1b-494a-433d-9370-9206ee1b5690	testcompany6	testcompany6@gmail.com	\N	\N	\N	\N	\N	f	2025-12-18 09:07:04.001899	2025-12-18 09:07:04.001904
630adcaf-a98b-4c03-93c8-71534c34025d	b39c1cb1-1269-40e9-a3b0-d962e6599357	testcompany7	testcompany7@gmail.com	\N	\N	\N	\N	\N	f	2025-12-18 09:08:24.937218	2025-12-18 09:08:24.937221
92975892-c9a2-45dd-98f9-352b9fd7ab81	fed24040-96ff-4da0-8ae8-a371e4fd136e	Quality Insight	qualitytvm@gmail.com	Prestige Tech Park, Tower B, 5th & 6th Floors\r\nMarathahalli - Outer Ring Road\r\nBangalore, Karnataka 560103			A strong company description includes several key components that help stakeholders understand the business and its value	Professional, Scientific, and Technical Activities	f	2025-12-13 08:36:19.116633	2025-12-18 11:25:56.521678
b62eb916-f156-4e15-99cf-4d1babf5fa6f	5f9f866b-374d-49a9-ab6e-a6a1d21d44e6	VR Tech Solutions Ltd.	vrtech@solutions.in	New Delhi				Administrative and Support Service Activities	f	2025-12-18 16:21:30.221615	2025-12-18 16:23:02.681465
a822ed9d-fab0-4761-9d41-e8983c11a4db	d8d64784-6edf-4b70-bad3-3d8cc54bd270	24gear	gearInida@gmail.com	\N	\N	\N	\N	\N	f	2025-12-27 05:22:31.774544	2025-12-27 05:22:31.774548
51c230ab-196c-467c-94b4-301e076f26f7	59344b9e-546f-4758-895f-f54195da6d02	vrtech	vrtech@gmail.com						f	2025-12-27 06:05:57.276458	2025-12-27 06:05:57.276463
57b48385-4d51-49a2-bf59-d1b642935a02	01b9049a-78d7-4dab-a398-4c4c6ab2412c	222	labs@example.com					Manufacturing	f	2025-12-27 05:36:55.817367	2025-12-27 08:09:10.407082
1aca7742-20b2-4adf-8598-5b21799d003a	b218045a-54f2-473f-a895-8f10b1a17026	22gear	gear@gmail.com	1234 Maple Street, Suite 567, Downtown Business District, Techville, CA 90210-1234, United States of America\nFlat 301, Tower B, Golden Heights Apartments, 789 Oak Avenue, Springfield, IL 62704, USA USA\n1234 Maple Street, Suite 567, Downtown Business District, Techville, CA 90210-1234, United States of America				Electricity, Gas, Steam, and Air Conditioning Supply	f	2025-12-27 05:34:42.737905	2025-12-27 08:09:31.267996
fab44ab2-0d23-4a67-903d-e9f28e70119a	a8328144-b540-4dbc-a3e5-705a7913cff7	InternationalConglomerateLtd	abcd@example.com						t	2025-12-27 05:43:41.41854	2025-12-27 08:10:30.829706
cc1d0a21-6565-4051-a53b-056a62e014ff	9afa7c4d-fca1-4b0b-8312-df94187bbeb3	TCC TVM	tcctvm@gmail.com	TechCore Consulting Headquarters: One Market Street, Suite 3600, Salesforce Tower, San Francisco, CA 94105-1001, United States. \r\nAdditional: PO Box 12345, SF Main. \r\nLandmarks: Opposite Ferry Building, near Embarcadero BART Station. \r\nDelivery Instructions: Use loading dock on Spear Street, business hours 9AM-5PM PST. \r\nSecurity: Check-in required at main lobby, photo ID mandatory. \r\nParking: Validated parking available at 75 Howard Street			TechCore Consulting (TCC) is a global leader in digital transformation solutions with 25+ years of excellence. We specialize in enterprise cloud migration, AI-driven analytics, cybersecurity frameworks, and custom software development. Our team of 500+ certified professionals delivers innovative solutions across healthcare, finance, retail, and manufacturing sectors. TCC's proprietary "Digital Maturity Framework" has helped 200+ Fortune 500 companies accelerate their digital journeys. Certified ISO 27001 and SOC 2 compliant, we prioritize data security while driving business innovation. Our mission: To empower organizations through cutting-edge technology, strategic consulting, and sustainable digital growth. Headquarters: San Francisco, with offices across 12 countries worldwide.Founded in 2010, we're a leading provider of innovative SaaS solutions for enterprise clients across multiple industries including finance, healthcare, and retail.Our mission is to transform business operation	Information and Communication	f	2025-12-18 09:00:56.46079	2025-12-27 08:47:24.992955
23644fd7-08bc-4375-8892-a799f87805e8	c873eef6-a5e4-40f7-abe7-844962d69b08	Sasta Global	sasta@gmail.com					Professional, Scientific, and Technical Activities	f	2025-12-27 09:06:39.284141	2025-12-27 09:08:13.395443
fc1588a2-4bf1-40d2-beb8-92b8bcbaf08a	3b7ce9fc-8d47-41c8-9c03-61ef7f1f668c	Quest Global	quest@example.com					Information and Communication	f	2025-12-27 17:16:03.787773	2025-12-28 08:11:43.582754
\.


--
-- Data for Name: communications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.communications (id, user_id, college_id, company_id, message, "timestamp", read_status, hidden) FROM stdin;
4284a813-4f9c-4fb8-86fa-ed5952fa0051	2032cdad-7746-4d7a-ad20-87a8a9b00fcd	\N	b2979fe8-89de-4042-aff9-a35d9d926887	Thank you for applying. We will review your profile.	2025-12-27 18:08:39.904857	t	f
66e2dac4-83c8-414f-b3f2-cb6842468945	2032cdad-7746-4d7a-ad20-87a8a9b00fcd	\N	b2979fe8-89de-4042-aff9-a35d9d926887	Thank you for applying. We will review your profile.	2025-12-27 18:15:01.317052	f	f
5b08bfd6-0af6-443f-9f9f-db26abd2e455	2032cdad-7746-4d7a-ad20-87a8a9b00fcd	\N	b2979fe8-89de-4042-aff9-a35d9d926887	Thank you for applying "Python Backend Developer". We will review your profile.	2025-12-27 18:16:56.261761	f	f
c273f0eb-b475-4ed2-8f88-f14e19e6ae4b	2032cdad-7746-4d7a-ad20-87a8a9b00fcd	\N	b2979fe8-89de-4042-aff9-a35d9d926887	Hi	2025-12-27 18:17:34.81042	f	t
0948c29a-7bfc-4f33-bea9-de39431ce0d3	2032cdad-7746-4d7a-ad20-87a8a9b00fcd	\N	b2979fe8-89de-4042-aff9-a35d9d926887	We would like to schedule an interview. Please let us know your availability.	2025-12-27 18:20:13.724026	f	f
70c3ad12-cc78-4b50-8399-a3a20400fecb	16399907-e0eb-429c-98f9-8159a1ba4fd0	\N	b2979fe8-89de-4042-aff9-a35d9d926887	Thank you for applying. We will review your profile.	2025-12-27 17:43:38.60792	f	t
36f52731-5b45-482a-9ee8-d8208dc0d94a	16399907-e0eb-429c-98f9-8159a1ba4fd0	\N	b2979fe8-89de-4042-aff9-a35d9d926887	Hi Aman,\r\nPlease Sent all your soft copies of your certicates to the mail "hruberinida@example.com"\r\nThanks	2025-12-28 07:42:53.572103	t	f
\.


--
-- Data for Name: coupons; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.coupons (id, code, faculty_id, year, college_id, created_at) FROM stdin;
d91d6861-8793-43da-a15d-c12f83fa7256	R3V3N1X6XL	CS5	2023	dd5c0787-62e7-4baf-b637-3c1b16d86a45	2025-12-18 17:07:55.848893
f9d4c1ce-5da2-420e-832d-22f61ebc042d	G8FWJWCZSH	cs5	2025	dd5c0787-62e7-4baf-b637-3c1b16d86a45	2025-12-18 17:08:46.632981
99e1e85d-2850-4ff2-ad5e-313e571d5c31	YG6CKVS34J	CS5	2022	eb49ce1e-c32a-4882-bc26-02d358aa6316	2025-12-18 17:09:47.750844
cb606e9b-724a-4f5c-9080-20f39089be94	XR23ZIWO87	CS5	2025	eb49ce1e-c32a-4882-bc26-02d358aa6316	2025-12-18 17:10:01.958388
4f08fced-58d7-4bff-862b-4a86ad3dbe9c	KB5GCZLKI2	20	1900	eb49ce1e-c32a-4882-bc26-02d358aa6316	2025-12-18 17:12:06.859117
4d01813b-cf3d-406d-b6ec-437e898bdbaf	NNE8QCKXEQ	ax-2344	2000	eb49ce1e-c32a-4882-bc26-02d358aa6316	2025-12-18 17:13:12.459331
4c634d91-26e9-4861-ae56-e0cda7b9bab5	GXPUK9IOT7	Ax4556	2002	eb49ce1e-c32a-4882-bc26-02d358aa6316	2025-12-18 17:13:37.956095
c76f9a13-77ab-4bbd-94ce-5762cb3f8740	ASODAHVV4P	Ax872	2004	eb49ce1e-c32a-4882-bc26-02d358aa6316	2025-12-18 17:13:48.765369
d39f2f44-1ef3-492b-bdb6-f011d93c2749	1HV33KP10R	AX42312	2006	eb49ce1e-c32a-4882-bc26-02d358aa6316	2025-12-18 17:14:00.68047
e43b0238-2f90-4f3a-bc0d-182c644e85d8	XGMNQ8S8SN	AS321312	2008	eb49ce1e-c32a-4882-bc26-02d358aa6316	2025-12-18 17:14:12.067319
983d549e-16a6-44b3-be19-16bf09cb1cad	UBE9OWQORR	12	2010	eb49ce1e-c32a-4882-bc26-02d358aa6316	2025-12-18 17:14:20.942847
daf0012e-2d83-456b-a90a-0e2c6ff6cff0	VY3WLM7TQD	A232	2012	eb49ce1e-c32a-4882-bc26-02d358aa6316	2025-12-18 17:14:49.561464
2b6f002e-aba8-4fbb-90ad-d996aa281c01	2C92EV2P25	22	2014	eb49ce1e-c32a-4882-bc26-02d358aa6316	2025-12-18 17:15:43.955061
e08cd73d-881e-4ae6-8f8e-397ea329ec10	CURK5GGGJN	CS28	2022	eb293b68-595b-4d67-9b19-45c5ad8a3f44	2025-12-27 09:10:00.878885
c45b28c8-38d9-4d2d-939a-223f6dedc672	O6K11TRCPO	AD123	2024	e801184a-e874-4467-9d13-042701aacd1b	2025-12-27 09:17:55.708307
\.


--
-- Data for Name: couponuser; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.couponuser (id, user_id, coupon_id, created_at) FROM stdin;
9476cb87-c841-479b-9850-71870106089e	82c879bd-3a41-4703-bbb9-b5f2f386405d	e08cd73d-881e-4ae6-8f8e-397ea329ec10	2025-12-27 09:10:21.944185
9fe41893-5a4b-4bb1-a8c1-6a070b0da1b8	1f3247f5-e9d8-49d6-870c-dab899925124	c45b28c8-38d9-4d2d-939a-223f6dedc672	2025-12-27 09:21:23.468791
64c4b768-f2cb-42b5-8784-0fc79b69f6d8	ecca8cf1-635b-4d81-8113-cb21f666e1b4	c45b28c8-38d9-4d2d-939a-223f6dedc672	2025-12-27 09:51:30.452636
1d6d640c-4063-4b7f-83eb-c2583ba34f1b	893b67a5-be80-42da-bb74-f0a4345976e7	c45b28c8-38d9-4d2d-939a-223f6dedc672	2025-12-27 09:53:23.822413
774ad9f0-3475-43d1-89ef-9739ef7cbaa2	33ab1367-1d38-4707-b2b1-5701dfd4c382	c45b28c8-38d9-4d2d-939a-223f6dedc672	2025-12-27 09:53:49.587978
3f273ef4-759d-4127-9bc7-bb1bc018a2a6	f4d4e565-1774-4b99-b4c3-541cd6946b9f	c45b28c8-38d9-4d2d-939a-223f6dedc672	2025-12-28 06:48:57.999745
9b9fb7e7-bf35-4dd8-bb08-e1e145963036	f076030b-e082-4dba-a866-e6a31f41416b	e08cd73d-881e-4ae6-8f8e-397ea329ec10	2025-12-28 07:36:46.353106
\.


--
-- Data for Name: jobs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.jobs (job_id, title, description, job_type, skills, years_of_exp, certifications, location, salary, total_vacancy, filled_vacancy, status, form_url, deadline, created_at, created_by, updated_at) FROM stdin;
55746acc-05f9-462a-b323-2a9dc14442c9	iOS Engineer	• Architect, design, and develop mobile libraries and sdks\r\n• Lead the development and optimization of mobile experiences using modern technologies\r\n• Understand and oversee the complex data workflows and pipelines, end-to-end.\r\n• Raise the bar in terms of observability, reliability and engineering best practices\r\n• Conduct code reviews, design discussions, and technical mentorship.\r\n• Collaborate with cross-functional teams to deliver comprehensive, end-to-end solutions.\r\n• Troubleshoot and resolve critical issues in production and development environments.\r\n• Provide strategic technical leadership to influence the direction of Uber’s technology stack.\r\n• Develop and maintain comprehensive documentation for software projects and processes.	Full-time	Proficiency in Swift and Objective-C, with extensive experience in SwiftUI and iOS frameworks. A strong understanding of architecture and -best practices in mobile development.\r\n• Hands-on experience with mobile web technologies is a plus.\r\n• Exceptional analytical skills to solve complex, high-scale technical challenges.\r\n• Demonstrated ability to lead projects, mentor engineers, and drive a culture of excellence and innovation.\r\n• Excellent collaborative and communication skills, with the ability to convey complex technical concepts.\r\n• Strong focus on high-quality mobile UI experiences and feature developments.\r\n• Previous contributions to creating major efficiencies or led cultural initiatives within your team or across several teams.\r\n• iOS Architecture, Tech Lead, Lead Architect, Team Lead\r\n• Work on mobile apps scaling to millions of users with experience managing these releases\r\n• Driving large scale initiatives that span multiple projects, teams, or groups of engineers.	1	iOS certification preferred	Bengaluru	30000	5	0	open		2025-12-14	2025-12-13 10:12:20.052292	b2979fe8-89de-4042-aff9-a35d9d926887	2025-12-13 10:13:10.587749
e551c943-a901-462e-9be5-2d099f88ba49	Software Developers Internships	Key Responsibilities\r\n\r\nAs part of the internship, you will work through a structured set of assignments designed to enhance your understanding of fintech principles and innovations. Your primary responsibilities will include :\r\n\r\nFintech Research\r\n• Research emerging fintech trends and technologies\r\n• Create competitive landscape analyses\r\n• Develop market opportunity assessments\r\n• Build innovation roadmap recommendations\r\n\r\nFinancial Product Analysis\r\n• Analyse digital financial products and services\r\n• Create user journey maps for financial applications\r\n• Develop feature comparison frameworks\r\n• Build product improvement recommendations\r\n\r\nTechnology Integration\r\n• Research technology solutions for financial services\r\n• Create proof-of-concept implementations\r\n• Develop integration frameworks\r\n• Build technology adoption strategies\r\n\r\nCustomer Experience\r\n• Analyse user experience in financial applications\r\n• Create customer engagement frameworks\r\n• Develop financial literacy content\r\n• Build digital onboarding approaches\r\n\r\nCapstone Project\r\n• Complete an end-to-end fintech project including : Market research, Product concept, Technology implementation plan, and User experience design\r\n\r\nWhat You Will Learn\r\n• Practical experience with fintech trends and applications\r\n• Digital financial product development\r\n• Technology integration in financial services\r\n• Customer experience design for financial applications\r\n• Innovation methodologies in fintech	Internship	• Student or fresh graduate from business, technology, finance, or related disciplines\r\n• Interest in the intersection of finance and technology\r\n• Adaptable and quick learning abilities\r\n• Strong communication and collaboration skills\r\n• Willingness to self-learn and work in a fast-paced environment	0				2	0	open		2025-12-19	2025-12-18 11:15:22.531205	b2979fe8-89de-4042-aff9-a35d9d926887	2025-12-18 11:15:22.531207
9132f52f-b068-4b5f-9646-eef126febb3a	Junior Data Analyst	We are seeking a Junior Data Analyst to assist in data collection, analysis, and reporting. Fresh graduates with strong analytical skills are encouraged to apply.	Full-time	Excel, SQL, Python (Basic), Data Visualization	1		Bangalore, Remote	₹4,00,000 per annum	1	0	open	https://companyname.com/data-analyst-questionnaire	2026-02-05	2025-12-27 09:31:30.035596	c873eef6-a5e4-40f7-abe7-844962d69b08	2025-12-27 09:39:54.940689
67039f51-de01-41b5-a52f-ac2175a6589d	Frontend Developer (React)	We are hiring a contract-based Frontend Developer to build responsive user interfaces using React. The role requires strong UI/UX understanding and performance optimization skills.	Part-time	React, JavaScript, HTML, CSS, Git, REST APIs	1	None	Remote	18,000/month	2	0	open	https://companyname.com/frontend-react-form	2025-12-31	2025-12-27 17:05:11.130201	67ec34eb-ea24-46b9-bcad-12dcb4f43499	2025-12-27 17:05:11.130206
74add033-80a8-4648-b0cd-4d82ed97c0a9	AI Agentic Developer Internship	Create AI-powered agents using n8n\r\n• Automate real business workflows (finance, operations, content, compliance, customer service and more)\r\n• Integrate GPT models, APIs, webhooks, databases, CRMs and custom logic\r\n• Work on live use cases from UAE businesses\r\n• Ship weekly agent deployments that prove your skills\r\n\r\nIdeal For\r\n• Students | Freshers | Career-switchers\r\n• Anyone excited about AI, automation and building portfolio-ready projects\r\n• Developers comfortable with Python/JS (bonus, not mandatory)	Full-time	Python\r\nJS	0		Trivandrum	8200	1	0	open		2025-12-28	2025-12-18 11:16:33.281611	b2979fe8-89de-4042-aff9-a35d9d926887	2025-12-27 17:19:19.504485
75476dd1-ef8b-40b3-b1f1-916d53b7c8dd	Staff Engineer	• Project Quark encompasses a complete redesign of the Fares Platform stack. Northstar for the project is to create a Fares platform that is resilient, LOB agnostic, easy to integrate and test, and supports rapid product innovation.\r\n• Inbounds: Enable various LOBs and partner teams to integrate with Fares platform to deliver a magical user experience.\r\n• Build out next gen observability tools for internal developers users of the Fares Platform through products and tools that make it a breeze to test, simulate, deploy and debug highly complex real time workflows at scale.	Full-time		0		Hyderabad		2	0	open		2025-12-31	2025-12-13 10:18:05.535606	b2979fe8-89de-4042-aff9-a35d9d926887	2025-12-27 17:20:09.148548
b07e1c0d-855d-41e1-8cd7-7f3d0ae46bfb	DevOps Engineer	Manage CI/CD pipelines, cloud infrastructure, and monitoring systems. Ensure system reliability and automate deployment processes.\r\nManage CI/CD pipelines, cloud infrastructure, and monitoring systems. Ensure system reliability and automate deployment processes.\r\nManage CI/CD pipelines, cloud infrastructure, and monitoring systems. Ensure system reliability and automate deployment processes.\r\nManage CI/CD pipelines, cloud infrastructure, and monitoring systems. Ensure system reliability and automate deployment processes.\r\nManage CI/CD pipelines, cloud infrastructure, and monitoring systems. Ensure system reliability and automate deployment processes.\r\nManage CI/CD pipelines, cloud infrastructure, and monitoring systems. Ensure system reliability and automate deployment processes.\r\nManage CI/CD pipelines, cloud infrastructure, and monitoring systems. Ensure system reliability and automate deployment processes.\r\nManage CI/CD pipelines, cloud infrastructure, and monitoring systems. Ensure system reliability and automate deployment processes.\r\nManage CI/CD pipelines, cloud infrastructure, and monitoring systems. Ensure system reliability and automate deployment processes.\r\nManage CI/CD pipelines, cloud infrastructure, and monitoring systems. Ensure system reliability and automate deployment processes.\r\nManage CI/CD pipelines, cloud infrastructure, and monitoring systems. Ensure system reliability and automate deployment processes.\r\nManage CI/CD pipelines, cloud infrastructure, and monitoring systems. Ensure system reliability and automate deployment processes.\r\nManage CI/CD pipelines, cloud infrastructure, and monitoring systems. Ensure system reliability and automate deployment processes.Manage CI/CD pipelines, cloud infrastructure, and monitoring systems. Ensure system reliability and automate deployment processes.\r\n....\r\n....\r\n....\r\n...\r\n....\r\n....\r\n...\r\n.....	Part-time	Linux, Docker, Kubernetes, AWS, Jenkins, Git	6		Remote	₹55,00,000/annum	1	0	open		2025-12-28	2025-12-27 17:23:54.26665	b2979fe8-89de-4042-aff9-a35d9d926887	2025-12-28 07:38:44.029514
187c4832-34d8-4c86-a4d0-125e850a6fb1	HR Executive	The HR Executive will manage recruitment activities, employee onboarding, payroll coordination, and HR documentation while ensuring compliance with company policies.	Full-time	Recruitment, Employee Engagement, HRMS, Communication Skills	0	MBA in Human Resources	Kochi, Coimbatore	₹3,50,000/annum	1	1	closed	https://companyname.com/hr-executive-form	2025-12-29	2025-12-27 17:18:01.703328	3b7ce9fc-8d47-41c8-9c03-61ef7f1f668c	2025-12-28 08:14:13.41774
7cca809b-abe4-4879-9d23-629373a8b773	Software Test Engineer	Key Responsibilities:\r\n\r\n● Understand software requirements and prepare detailed test scenarios and test cases.\r\n● Perform manual testing to identify and document defects.\r\n● Assist in test execution, regression testing, and defect verification.\r\n● Collaborate with developers and other QA team members to ensure software quality.\r\n● Learn and adapt to testing tools, automation frameworks, and best practices.\r\n● Ensure testing activities align with project timelines and quality standards.	Full-time	Preferred Skills:\r\n\r\n● Educational Qualification:\r\n● Bachelor's degree (B.Tech / B.E / B.Sc / BCA / M.Sc / MCA) in Computer Science, Information Technology, or related field.\r\n● Good understanding of Software Development Life Cycle (SDLC) and Software Testing Life Cycle (STLC).\r\n● Basic knowledge of testing concepts, test case design, and defect management.\r\n● Exposure to manual testing (and automation basics preferred).\r\n● Strong analytical, logical, and problem-solving skills.\r\n● Good verbal and written communication skills.\r\n● Positive attitude, eagerness to learn, and ability to work effectively in a team.	0	● ISTQB Foundation Level Certification (preferred).\r\n● Exposure to any testing tools (e.g., JIRA, Postman, Selenium) during training or academic projects.\r\n● Basic programming knowledge (in Java, Python, or JavaScript).\r\n● Internship or project experience in software testing	Trivandrum	20000	1	0	open		2027-01-03	2025-12-18 11:21:51.783583	fed24040-96ff-4da0-8ae8-a371e4fd136e	2025-12-18 11:21:51.783585
a38a7088-f280-46f0-adec-d528a32d8de6	Software Engineer	0 to 1 year working experience in product / services industry with strong technical knowledge.Knowledge in one or more languages like .Net, C#, JavaScript, VBScript, REST Services, PL/SQL.Ability to work independently and with assisted supervisionStrong interpersonal skills with proven experience building strong interpersonal relationshipsExcellent verbal and written communication skillsStrong analytical and problem-solving abilities,Results oriented with creative abilities, sense of urgency and passionStrong experience with Microsoft product suite including PowerPoint, Word, Excel, ProjectBachelor / Maters degree in an appropriate subject (e.g. computer science, or engineering) is required.	Contract	Knowledge in one or more languages like .Net, \r\nC#, \r\nJavaScript, \r\nVBScript, \r\nREST Services, \r\nPL/SQL	0		Thiruvananthapuram	24000	2	0	open		2025-12-19	2025-12-18 11:25:26.853058	fed24040-96ff-4da0-8ae8-a371e4fd136e	2025-12-18 11:25:26.85306
b46dffa7-7ac5-4f77-a444-cb77b64c8183	Java Spring boot Developer	We are currently planning to do F2F Interview on 20th –Dec- 2025 (Saturday)\r\n\r\nHyderabad Drive Location : Tata Consultancy Services, CMC-Non Sez, Synergy Park non-SEZ (Old CMC Building), Opposite to DLF building, Gachibowli, Hyderabad 500032.\r\n\r\nChennai Drive Location : TCS SNR-Kumaran Nagar, 415 / 21-24, TNHB Main Rd, Chennai, Tamil Nadu 600119.	Full-time	6+ years of software engineering experience.\r\n\r\n6+ years’ experience writing, debugging, and troubleshooting code in mainstream Java and Spring Boot.\r\n\r\n6+ years’ experience with Cloud technology : GCP, AWS, or Azure.\r\n\r\n6+ years’ experience designing and developing cloud-native solutions.\r\n\r\n6+ years’ experience designing and developing microservices using Java, Spring Boot, GCP SDKs, GKE / Kubernetes.\r\n• 6+ years’ experience designing and developing big data processing solutions using Dataflow / Apache Beam, Bigtable, Big Query, Pub Sub, GCS, Composer / Airflow, and others.\r\n\r\n6+ years’ experience deploying and releasing software using Jenkins CI / CD pipelines, understanding infrastructure-as-code concepts, Helm Charts, and Terraform constructs.	6		Hyderabad / Chennai	100000	1	0	open		2025-12-19	2025-12-18 11:34:01.519779	9afa7c4d-fca1-4b0b-8312-df94187bbeb3	2025-12-18 11:34:01.519787
335429aa-f83b-4b68-842f-c7c70a550cb2	Java Full-Stack Developer	• 6+ years of experience Develops secure and high-quality production code, and reviews and debugs codes.\r\n• Actively contributes to the engineering community as an advocate of firmwide frameworks, tools, and practices of the Software Development Life Cycle\r\n• Influences peers and project decision-makers to consider the use and application of leading-edge technologies.\r\n• Technologies experience: Java 8 or 11, AWS or Azure, Microservices, MongoDB, REST APIS, microservices\r\n• 80% backend and 20% frontend-Front end is React, Javascript\r\n• Kafka is good to have	Contract		6		PAN India		1000	0	open		2025-12-19	2025-12-18 11:35:34.065118	9afa7c4d-fca1-4b0b-8312-df94187bbeb3	2025-12-18 11:35:34.065123
b5cef615-66a9-4520-910a-64bf455d785b	React Developer	• Strong proficiency in TypeScript.\r\n• Solid understanding of JSX and the React component lifecycle.\r\n• Familiarity with React Hooks (e.g., useState, useEffect, useContext).\r\n• Experience with state management libraries (Redux, Zustand, or Context API).\r\n• Understanding of RESTful APIs or GraphQL.\r\n• Proficiency in HTML5, CSS3, and responsive design principles.\r\n• Experience with version control systems like Git.\r\n• Ability to mentor or support Angular developers transitioning to React.\r\n• Experience working in mixed-technology environments (React + Angular).\r\n• Good communication skills for cross-team collaboration.	Part-time	- Strong expertise in React.js and Next.js (SSR, SSG, API routes)\r\n\r\n- Proficiency in JavaScript (ES6+), HTML5, CSS3, and Tailwind CSS\r\n\r\n- Proficiency in css pre-processors\r\n\r\n- Experience with state management libraries such as Redux, Zustand, or Recoil\r\n\r\n- Solid understanding of build tools like Webpack or Vite\r\n\r\n- Familiarity with Git workflow and collaborative version control	1		Remote	25000	2	0	open	https://docs.google.com/forms/d/e/1FAIpQLSfWLD9EnEPRxx9mp-wPPoBQKjp1jE6gOZrqOTq7AnBKfao-tg/viewform?usp=header	2025-12-19	2025-12-18 16:44:15.131237	5f9f866b-374d-49a9-ab6e-a6a1d21d44e6	2025-12-18 16:44:15.131244
f7d69c28-0174-48d8-8974-1e7cfce57ee8	Software Engineer	We are looking for a Software Engineer responsible for developing, testing, and maintaining web-based applications. The candidate should be able to work collaboratively with cross-functional teams and follow best coding practices.	Full-time	Java, \r\nSpring Boot, \r\nREST API, \r\nSQL, \r\nGit, \r\nHTML, \r\nCSS	2	Oracle Certified Java Programmer,\r\nScrum Master	Bangalore, Hyderabad, Chennai	₹6,00,000 – ₹8,00,00	3	0	open	https://sasta.com/software-engineer-questionnaire	2025-12-28	2025-12-27 09:25:55.867844	c873eef6-a5e4-40f7-abe7-844962d69b08	2025-12-27 09:25:55.867846
0ae3dadb-9593-49d7-84e0-5e1b2c591cab	1 Angular Developer	12345678910	Part-time		22		remote	2 per hour	1	0	open		2026-01-10	2025-12-18 16:54:04.963417	9afa7c4d-fca1-4b0b-8312-df94187bbeb3	2025-12-18 17:00:56.486428
cef40b04-092d-4b45-a011-647763456546	Senior QA Automation Engineer	The QA Automation Engineer will be responsible for designing, executing, and maintaining automated test scripts for web applications. The role involves close collaboration with developers and product teams.	Contract	Selenium, Java, TestNG, API Testing, Postman, SQL	2	ISTQB Foundation Level	Trivandrum	45,000	1	0	open	https://companyname.com/qa-automation-questionnaire	2025-12-27	2025-12-27 09:31:34.816923	c873eef6-a5e4-40f7-abe7-844962d69b08	2025-12-27 09:38:08.338659
4a8beef4-ac3a-45d7-88bb-baea4e1ef1be	QA Automation Engineer-1	The QA Automation Engineer will be responsible for designing, executing, and maintaining automated test scripts for web applications. The role involves close collaboration with developers and product teams.	Full-time	Selenium, Java, TestNG, API Testing, Postman, SQL	0	ISTQB Foundation Level	Trivandrum, Kochi, Remote	₹7,50,000 per annum	1	0	open	https://companyname.com/qa-automation-questionnaire	2025-12-28	2025-12-27 09:31:39.028392	c873eef6-a5e4-40f7-abe7-844962d69b08	2025-12-27 09:56:50.888055
d1c47688-4156-418a-92e0-9e96a536c1e2	FULL STACK-Intern	We are looking for enthusiastic Full Stack Developer Interns who are eager to learn and build modern web applications. You will work closely with our development team to design, develop, and deploy full-stack projects using the latest technologies.\r\n\r\nKey Responsibilities:\r\n• Assist in developing front-end and back-end features for web applications.\r\n• Collaborate with the team to design and implement APIs and databases.\r\n• Debug, test, and maintain code quality across the application.\r\n• Learn and work with frameworks like Laravel, React, or Node.js (based on project needs).\r\n• Participate in team meetings, brainstorming sessions, and code reviews.\r\nEligibility : \r\n• Freshers or Final Year Students (BCA / BSc CS / BE / B.Tech / MCA).\r\n• Passionate about building a career in web development.	Internship	Required Skills:\r\n• Basic knowledge of HTML, CSS, JavaScript, PHP, MySQL.\r\n• Familiarity with frameworks like Laravel or React.js is a plus.\r\n• Strong problem-solving and communication skills.\r\n• Willingness to learn and adapt to new technologies.	0		Trivandrum	₹10,000.00 - ₹20,000	4	0	open		2025-12-31	2025-12-18 11:30:58.628887	67ec34eb-ea24-46b9-bcad-12dcb4f43499	2025-12-27 17:11:48.791479
c8be6a29-f3c0-4a83-a78c-0c5dfc97b57f	Python Backend Developer	Design and develop scalable backend services, APIs, and database integrations. Ensure high performance and security of applications.	Part-time	Python, Django, REST API, PostgreSQL, Git	1	AWS Certified Developer – Associate	Pune, Bangalore	₹8,00,000/annum	1	1	closed	https://companyname.com/backend-engineer-questionnaire	2026-01-01	2025-12-27 17:23:49.1843	b2979fe8-89de-4042-aff9-a35d9d926887	2025-12-28 07:07:16.743983
\.


--
-- Data for Name: favorites; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.favorites (id, user_id, job_id, saved_at) FROM stdin;
00e36553-7c6a-46cb-b7db-83c85d82f2ab	82c879bd-3a41-4703-bbb9-b5f2f386405d	4a8beef4-ac3a-45d7-88bb-baea4e1ef1be	2025-12-27 09:43:30.30416
fc42ed69-1240-48ad-a0d2-2408ee5184d7	82c879bd-3a41-4703-bbb9-b5f2f386405d	7cca809b-abe4-4879-9d23-629373a8b773	2025-12-27 09:49:00.271658
9c897bf2-7921-4f1a-9e54-ea55725ffa4d	33ab1367-1d38-4707-b2b1-5701dfd4c382	d1c47688-4156-418a-92e0-9e96a536c1e2	2025-12-27 17:13:52.916355
68c17c6b-aacc-4a04-957a-de393963c399	33ab1367-1d38-4707-b2b1-5701dfd4c382	9132f52f-b068-4b5f-9646-eef126febb3a	2025-12-27 17:14:13.037207
6e9a9c9a-ea31-4878-bb41-31545f741dd2	33ab1367-1d38-4707-b2b1-5701dfd4c382	4a8beef4-ac3a-45d7-88bb-baea4e1ef1be	2025-12-27 17:14:22.259112
1824b321-d0f8-4402-9569-96efd44b638e	01166ff5-cf0b-4c54-a384-6aa006ce7fc7	b07e1c0d-855d-41e1-8cd7-7f3d0ae46bfb	2025-12-27 17:29:13.583377
c82459ac-ecfe-45c2-aa39-6ce2ffc86727	01166ff5-cf0b-4c54-a384-6aa006ce7fc7	c8be6a29-f3c0-4a83-a78c-0c5dfc97b57f	2025-12-27 17:29:18.588683
9fd49849-52e8-4057-88ce-543f630068cc	33ab1367-1d38-4707-b2b1-5701dfd4c382	b07e1c0d-855d-41e1-8cd7-7f3d0ae46bfb	2025-12-27 17:29:45.31226
9cc6934e-d4b5-4bd9-a30d-d09161882d83	33ab1367-1d38-4707-b2b1-5701dfd4c382	c8be6a29-f3c0-4a83-a78c-0c5dfc97b57f	2025-12-27 17:29:47.783238
a74fe8b2-fefc-4ee6-8693-1aeda27a8878	f076030b-e082-4dba-a866-e6a31f41416b	b07e1c0d-855d-41e1-8cd7-7f3d0ae46bfb	2025-12-27 18:23:34.732435
\.


--
-- Data for Name: job_applications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.job_applications (id, user_id, job_id, status, resume_path, date_applied, status_updated_at) FROM stdin;
aacf18bc-13e3-49c3-ae85-31258717b1f3	01166ff5-cf0b-4c54-a384-6aa006ce7fc7	c8be6a29-f3c0-4a83-a78c-0c5dfc97b57f	Rejected	static/uploads/resume_aman_1page_doc.docx	2025-12-27 17:29:23.026911	2025-12-28 06:41:51.596247
b0b5d5f3-3236-46f3-a485-009260e8b56e	82c879bd-3a41-4703-bbb9-b5f2f386405d	4a8beef4-ac3a-45d7-88bb-baea4e1ef1be	Pending	static/uploads/resume_SINOJ GEORGE_resume.pdf	2025-12-27 09:44:57.796479	2025-12-27 09:44:57.796487
c0d4fe73-d376-4832-bc96-faf012ce7d31	1f3247f5-e9d8-49d6-870c-dab899925124	4a8beef4-ac3a-45d7-88bb-baea4e1ef1be	Pending	static/uploads/resume_arun_sample10page.pdf	2025-12-27 09:48:14.463131	2025-12-27 09:48:14.463137
a3caf0d0-927f-4b57-9919-b35eb8daf021	1f3247f5-e9d8-49d6-870c-dab899925124	9132f52f-b068-4b5f-9646-eef126febb3a	Pending	static/uploads/resume_arun_sample10page.pdf	2025-12-27 09:48:22.745003	2025-12-27 09:48:22.745019
5a6827a6-cb60-4874-b9a8-e6716a87c1a9	33ab1367-1d38-4707-b2b1-5701dfd4c382	7cca809b-abe4-4879-9d23-629373a8b773	Pending	static/uploads/resume_Aparna Asok_1pagepdf.pdf	2025-12-27 10:00:19.496305	2025-12-27 10:00:19.496308
53b86f1e-08d7-4e76-91f6-9ebf3979b800	01166ff5-cf0b-4c54-a384-6aa006ce7fc7	67039f51-de01-41b5-a52f-ac2175a6589d	Pending	static/uploads/resume_aman_1page_doc.docx	2025-12-27 17:07:49.669632	2025-12-27 17:07:49.669639
36a98c8d-728e-4198-8608-a8c3a645c353	01166ff5-cf0b-4c54-a384-6aa006ce7fc7	f7d69c28-0174-48d8-8974-1e7cfce57ee8	Pending	static/uploads/resume_aman_1page_doc.docx	2025-12-27 17:08:01.593337	2025-12-27 17:08:01.593343
2092c4c1-b9f5-4e13-91e1-7f64a86640b9	33ab1367-1d38-4707-b2b1-5701dfd4c382	d1c47688-4156-418a-92e0-9e96a536c1e2	Pending	static/uploads/resume_Aparna Asok_1pagepdf.pdf	2025-12-27 17:13:41.161399	2025-12-27 17:13:41.161402
2acebdb9-4a99-47dc-8767-4a21adb1c856	33ab1367-1d38-4707-b2b1-5701dfd4c382	9132f52f-b068-4b5f-9646-eef126febb3a	Pending	static/uploads/resume_Aparna Asok_1pagepdf.pdf	2025-12-27 17:14:08.463886	2025-12-27 17:14:08.463888
8dc9cc28-8ca4-44ac-a6a7-3245e91a217f	33ab1367-1d38-4707-b2b1-5701dfd4c382	4a8beef4-ac3a-45d7-88bb-baea4e1ef1be	Pending	static/uploads/resume_Aparna Asok_1pagepdf.pdf	2025-12-27 17:14:17.105102	2025-12-27 17:14:17.105109
3f140262-1e44-49eb-90f7-887b5983bd29	33ab1367-1d38-4707-b2b1-5701dfd4c382	0ae3dadb-9593-49d7-84e0-5e1b2c591cab	Pending	static/uploads/resume_Aparna Asok_1pagepdf.pdf	2025-12-27 17:47:57.567672	2025-12-27 17:47:57.567683
d54e0df2-d92c-4030-a5dd-3dd22c2f3879	33ab1367-1d38-4707-b2b1-5701dfd4c382	67039f51-de01-41b5-a52f-ac2175a6589d	Pending	static/uploads/resume_Aparna Asok_1pagepdf.pdf	2025-12-27 18:09:55.870059	2025-12-27 18:09:55.870062
5c305ca2-df27-4396-be96-6f09dc40229e	33ab1367-1d38-4707-b2b1-5701dfd4c382	f7d69c28-0174-48d8-8974-1e7cfce57ee8	Pending	static/uploads/resume_Aparna Asok_1pagepdf.pdf	2025-12-27 18:10:05.480809	2025-12-27 18:10:05.480812
703a1549-7af1-47ba-bc9c-3685e591d229	01166ff5-cf0b-4c54-a384-6aa006ce7fc7	b07e1c0d-855d-41e1-8cd7-7f3d0ae46bfb	Interviewed	static/uploads/resume_aman_1page_doc.docx	2025-12-27 17:29:15.515987	2025-12-27 18:20:50.00277
9a58e58f-aaec-47ab-8a0c-3cc6fb890b63	33ab1367-1d38-4707-b2b1-5701dfd4c382	c8be6a29-f3c0-4a83-a78c-0c5dfc97b57f	Hired	static/uploads/resume_Aparna Asok_1pagepdf.pdf	2025-12-27 18:09:45.500102	2025-12-28 07:07:16.727424
ebe08c12-f7fa-4f5b-bd33-b2924fec832c	1f3247f5-e9d8-49d6-870c-dab899925124	b07e1c0d-855d-41e1-8cd7-7f3d0ae46bfb	Pending	static/uploads/resume_arun_sample10page.pdf	2025-12-27 18:25:54.319691	2025-12-27 18:25:54.319694
447f4609-a951-4a1a-80ba-a5d4895755af	33ab1367-1d38-4707-b2b1-5701dfd4c382	b07e1c0d-855d-41e1-8cd7-7f3d0ae46bfb	Interviewed	static/uploads/resume_Aparna Asok_1pagepdf.pdf	2025-12-27 17:29:54.092793	2025-12-28 07:11:06.446249
30719ab1-65f7-4814-8d19-9fd96e27a900	f4d4e565-1774-4b99-b4c3-541cd6946b9f	b07e1c0d-855d-41e1-8cd7-7f3d0ae46bfb	Interviewed	static/uploads/resume_kavya_sample10page.pdf	2025-12-28 06:51:44.309773	2025-12-28 07:29:35.736436
7a0f93cd-d7af-42cf-9e89-e3055b3be807	01166ff5-cf0b-4c54-a384-6aa006ce7fc7	9132f52f-b068-4b5f-9646-eef126febb3a	Pending	static/uploads/resume_aman_1page_doc.docx	2025-12-28 07:40:57.228137	2025-12-28 07:40:57.22814
805da552-b7b2-4ee1-83c9-edb43216e3cc	01166ff5-cf0b-4c54-a384-6aa006ce7fc7	74add033-80a8-4648-b0cd-4d82ed97c0a9	Interviewed	static/uploads/resume_aman_1page_doc.docx	2025-12-27 18:11:26.277485	2025-12-28 07:41:32.666363
e0f3e48e-981f-4642-80b8-4612545c4d58	f4d4e565-1774-4b99-b4c3-541cd6946b9f	187c4832-34d8-4c86-a4d0-125e850a6fb1	Hired	static/uploads/resume_kavya_sample10page.pdf	2025-12-28 07:04:27.130795	2025-12-28 08:14:13.412491
eedbd83d-fd88-4e5e-b8e7-d74a07d9dedb	33ab1367-1d38-4707-b2b1-5701dfd4c382	187c4832-34d8-4c86-a4d0-125e850a6fb1	Hired	static/uploads/resume_Aparna Asok_1pagepdf.pdf	2025-12-27 18:09:50.386385	2025-12-28 08:15:34.479229
\.


--
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notifications (id, user_id, company_id, message, read_status, hidden, "timestamp") FROM stdin;
d7c2bb76-59d3-446b-934b-d163cea316b3	e6038c34-e922-41df-9aaf-e035f80601e1	c873eef6-a5e4-40f7-abe7-844962d69b08	SINOJ GEORGE has applied for the job: QA Automation Engineer	f	f	2025-12-27 09:44:57.798825
a96c22b2-c4c6-4417-b660-19b4b5d1ea0d	17bdd5c4-e1e4-4ef7-bb56-971d0454b3f2	c873eef6-a5e4-40f7-abe7-844962d69b08	arun has applied for the job: QA Automation Engineer	f	f	2025-12-27 09:48:14.464678
cbd9d9b7-cdc5-41de-98f2-96c9a766fb57	17bdd5c4-e1e4-4ef7-bb56-971d0454b3f2	c873eef6-a5e4-40f7-abe7-844962d69b08	arun has applied for the job: Junior Data Analyst	f	f	2025-12-27 09:48:22.746582
07c5bc8d-0e42-434d-9592-49bb1352a02b	2032cdad-7746-4d7a-ad20-87a8a9b00fcd	fed24040-96ff-4da0-8ae8-a371e4fd136e	Aparna Asok has applied for the job: Software Test Engineer	f	f	2025-12-27 10:00:19.497377
bc27b8dd-4566-42bf-94ca-4eba0226cc71	16399907-e0eb-429c-98f9-8159a1ba4fd0	67ec34eb-ea24-46b9-bcad-12dcb4f43499	aman has applied for the job: Frontend Developer (React)	f	f	2025-12-27 17:07:49.672829
33212ce7-9107-44b7-8482-ea4aa471f91e	16399907-e0eb-429c-98f9-8159a1ba4fd0	c873eef6-a5e4-40f7-abe7-844962d69b08	aman has applied for the job: Software Engineer	f	f	2025-12-27 17:08:01.594626
30b921c9-53b4-4e10-87da-0ab81b600f0d	2032cdad-7746-4d7a-ad20-87a8a9b00fcd	67ec34eb-ea24-46b9-bcad-12dcb4f43499	Aparna Asok has applied for the job: FULL STACK-Intern	f	f	2025-12-27 17:13:41.162967
78a817b3-f946-4cbf-9aa1-f9ac9d307fef	2032cdad-7746-4d7a-ad20-87a8a9b00fcd	c873eef6-a5e4-40f7-abe7-844962d69b08	Aparna Asok has applied for the job: Junior Data Analyst	f	f	2025-12-27 17:14:08.465459
8f8a633e-3b18-4b4a-92d0-4d3be62c3772	2032cdad-7746-4d7a-ad20-87a8a9b00fcd	c873eef6-a5e4-40f7-abe7-844962d69b08	Aparna Asok has applied for the job: QA Automation Engineer-1	f	f	2025-12-27 17:14:17.106777
2b67b72b-5c0b-4a8e-b72a-287d6bd03cd7	16399907-e0eb-429c-98f9-8159a1ba4fd0	b2979fe8-89de-4042-aff9-a35d9d926887	aman has applied for the job: DevOps Engineer	f	f	2025-12-27 17:29:15.516752
acd2ea1e-717c-449d-a206-22a9733d3625	16399907-e0eb-429c-98f9-8159a1ba4fd0	b2979fe8-89de-4042-aff9-a35d9d926887	aman has applied for the job: Python Backend Developer	f	f	2025-12-27 17:29:23.027969
b4945a73-7203-43c7-818e-bc108ea0488a	2032cdad-7746-4d7a-ad20-87a8a9b00fcd	b2979fe8-89de-4042-aff9-a35d9d926887	Aparna Asok has applied for the job: DevOps Engineer	f	f	2025-12-27 17:29:54.093408
b90d74dd-cb25-47d3-84ec-a0168dabfe36	2032cdad-7746-4d7a-ad20-87a8a9b00fcd	9afa7c4d-fca1-4b0b-8312-df94187bbeb3	Aparna Asok has applied for the job: 1 Angular Developer	f	f	2025-12-27 17:47:57.568706
a5a5abf3-5bc7-4e4f-9655-1d5fb2810d10	2032cdad-7746-4d7a-ad20-87a8a9b00fcd	b2979fe8-89de-4042-aff9-a35d9d926887	Aparna Asok has applied for the job: Python Backend Developer	f	f	2025-12-27 18:09:45.501003
3a2fca0e-5431-47bf-899e-6753995e1186	2032cdad-7746-4d7a-ad20-87a8a9b00fcd	3b7ce9fc-8d47-41c8-9c03-61ef7f1f668c	Aparna Asok has applied for the job: HR Executive	f	f	2025-12-27 18:09:50.387245
55e02855-ca65-492e-9d53-3c73bb02adaa	2032cdad-7746-4d7a-ad20-87a8a9b00fcd	67ec34eb-ea24-46b9-bcad-12dcb4f43499	Aparna Asok has applied for the job: Frontend Developer (React)	f	f	2025-12-27 18:09:55.870712
9605599f-d7c9-44a5-b0dd-506ea8ed413e	2032cdad-7746-4d7a-ad20-87a8a9b00fcd	c873eef6-a5e4-40f7-abe7-844962d69b08	Aparna Asok has applied for the job: Software Engineer	f	f	2025-12-27 18:10:05.481689
3a119fda-f7cb-4ebf-83d2-659dc03cbe9a	16399907-e0eb-429c-98f9-8159a1ba4fd0	b2979fe8-89de-4042-aff9-a35d9d926887	aman has applied for the job: AI Agentic Developer Internship	f	f	2025-12-27 18:11:26.279095
d01150c5-49de-4c63-8bca-bea2e4e93af5	17bdd5c4-e1e4-4ef7-bb56-971d0454b3f2	b2979fe8-89de-4042-aff9-a35d9d926887	arun has applied for the job: DevOps Engineer	f	f	2025-12-27 18:25:54.321089
2bd2fa36-5e47-4b59-9628-be0a73fa2920	698c652d-1371-4e0f-9bb7-1a391f6210a3	b2979fe8-89de-4042-aff9-a35d9d926887	kavya has applied for the job: DevOps Engineer	f	f	2025-12-28 06:51:44.31507
fd6496ec-f127-4a9d-a3bb-268f0b920c85	698c652d-1371-4e0f-9bb7-1a391f6210a3	3b7ce9fc-8d47-41c8-9c03-61ef7f1f668c	kavya has applied for the job: HR Executive	f	f	2025-12-28 07:04:27.132738
ff35d1c1-dc19-4f01-869b-bad387682406	16399907-e0eb-429c-98f9-8159a1ba4fd0	c873eef6-a5e4-40f7-abe7-844962d69b08	aman has applied for the job: Junior Data Analyst	f	f	2025-12-28 07:40:57.228911
\.


--
-- PostgreSQL database dump complete
--

