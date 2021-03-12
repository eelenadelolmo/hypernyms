import shutil
import json
import os

dir_all = 'corpus/Medical/txt_all.txt'
dir_texts = 'corpus/Medical/txt'

shutil.rmtree(dir_texts, ignore_errors=True)
os.makedirs(dir_texts + '/')

txt_all = ''

with open('corpus/Medical/OutPretty.json') as f:

	texto = f.read()
	texto_json = json.loads(texto)

	for elem in texto_json:

		txt = ''

		if 'exam' in [x for x in elem]:
			txt_all += elem['exam'] + '\r\n'
			txt += elem['exam'] + '\r\n'
		if 'txFollowup' in [x for x in elem]:
			txt_all += elem['txFollowup'] + '\r\n'
			txt += elem['txFollowup'] + '\r\n'
		if 'findings' in [x for x in elem]:
			txt_all += elem['findings'] + '\r\n'
			txt += elem['findings'] + '\r\n'
		if 'diagnosis' in [x for x in elem]:
			txt_all += elem['diagnosis'] + '\r\n'
			txt += elem['diagnosis'] + '\r\n'
		if 'ddx' in [x for x in elem]:
			txt_all += elem['ddx'] + '\r\n'
			txt += elem['ddx'] + '\r\n'
		if 'history' in [x for x in elem]:
			txt_all += elem['history'] + '\r\n'
			txt += elem['history'] + '\r\n'
		if 'discussion' in [x for x in elem]:
			txt_all += elem['discussion'] + '\r\n'
			txt += elem['discussion'] + '\r\n'

		txt_all += '\r\n\r\n\r\n\r\n'

		if 'mCaseID' in [x for x in elem]:
			id = elem['mCaseID']
			with open(dir_texts + '/' + id + '.txt', 'w') as f_w:
				f_w.write(txt)

with open(dir_all, 'w') as f_w:
	f_w.write(txt_all)
