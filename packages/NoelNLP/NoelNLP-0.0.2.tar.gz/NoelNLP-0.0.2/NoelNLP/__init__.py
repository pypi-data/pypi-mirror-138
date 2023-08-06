def stopList():
    try:
        stop_word_list = ['na', 'lakini', 'ingawa', 'ingawaje', 'kwa', 'sababu', 'hadi', 'hata', 'kama', 'ambapo', 'ambamo', 'ambako', 'ambacho', 'ambao', 'ambaye', 'ilhali', 'ya', 'yake', 'yao', 'yangu', 'yetu', 'yenu', 'vya', 'vyao', 'vyake', 'vyangu', 'vyenu', 'vyetu', 'yako', 'hizo', 'mimi', 'sisi', 'wewe', 'nyinyi', 'yeye', 'wao', 'nao', 'nasi', 'nanyi', 'ni', 'alikuwa', 'atakuwa', 'hii', 'hizi', 'zile', 'ile', 'hivi', 'vile', 'za', 'zake', 'zao', 'zenu', 'kwenye', 'katika', 'kwao', 'kwenu', 'kwetu', 'dhidi', 'kati', 'miongoni', 'katikati', 'wakati', 'kabla', 'baada', 'baadaye', 'nje', 'tena', 'mbali', 'halafu', 'hapa', 'pale', 'mara', 'yoyote', 'wowote', 'chochote', 'vyovyote', 'yeyote', 'lolote', 'mwenye', 'mwenyewe', 'lenyewe', 'lenye', 'wote', 'lote', 'vyote', 'nyote', 'kila', 'zaidi', 'hapana', 'ndiyo', 'au', 'ama', 'sio', 'siye', 'tu', 'budi', 'nyingi', 'nyingine', 'wengine', 'mwingine', 'zingine', 'lingine', 'kingine', 'chote', 'sasa', 'basi', 'bila', 'cha', 'chini', 'hapo', 'huku', 'kule', 'humu', 'hivyo', 'hivyohivyo', 'vivyo', 'palepale', 'fauka', 'hiyo', 'hiyohiyo', 'zilezile', 'hao', 'haohao', 'hukuhuku', 'humuhumu', 'huko', 'hukohuko', 'huo', 'huohuo', 'hili', 'hilihili', 'ilikuwa', 'juu', 'karibu', 'kima', 'kisha', 'kutoka', 'kwenda', 'kubwa', 'ndogo', 'kwamba', 'kuwa', 'la', 'lao', 'lo', 'mdogo', 'mkubwa', 'ng’o', 'pia', 'aidha', 'vilevile', 'kadhalika', 'halikadhalika', 'sana', 'pamoja', 'tafadhali', 'wa', 'wake', 'yule', 'wale', 'zangu', 'afanaleki', 'salale', 'oyee', 'yupi', 'ipi', 'lipi', 'ngapi', 'si', 'angali', 'wangali', 'loo', 'ohoo', 'barabara', 'ewaa', 'walahi', 'masalale', 'duu', 'toba', 'mh', 'kumbe', 'ala', 'ebo', 'haraka', 'pole', 'polepole', 'harakaharaka', 'itakuwa', 'mtakuwa', 'tutakuwa', 'labda', 'yumkini', 'haiyumkini', 'yapata', 'takribani', 'hususani', 'yawezekana', 'nani', 'ndani', 'baadhi', 'kuliko', 'mwa', 'hasha', 'moja', 'pili', 'kwanza', 'ili', 'je', 'jinsi', 'ila', 'nini', 'hasa', 'huu', 'zako', 'alisema', 'walikuwa', 'naye', 'watu', 'sauti', 'akasema', 'baadae', 'muda', 'mrefu', 'akatokea', 'akaja', 'wangu', 'kikubwa', 'kiasi', 'mmoja', 'kidogo', 'mpaka']
        return stop_word_list
    except Exception as e:
        print('Something Is Wrong')	


def stopRemover(x):
	try:
		print('Hi %s Am Stop Words'%x)
	except Exception as e:
		print('Something Is Wrong')	


def moseStemmer(x):
	try:
		print('Hi %s Am Swahili Stemmer'%x)
	except Exception as e:
		print('Something Is Wrong')	    


