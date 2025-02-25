#!/usr/bin/env python

from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, PlainTextResponse
import uvicorn
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from typing import Optional
import enum
from ramda import *
from pathlib import Path
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse, PlainTextResponse
import json
from typing import List

# CONFIG
TASK = 'translation'
CKPT = 'facebook/nllb-200-distilled-600M'

MAX_LEN = 512
# RUN


Languages = enum.Enum('languages', {name: name for name in [ "ace_Arab", "ace_Latn", "acm_Arab", "acq_Arab", "aeb_Arab", "afr_Latn", "ajp_Arab", "aka_Latn", "amh_Ethi", "apc_Arab", "arb_Arab", "ars_Arab", "ary_Arab", "arz_Arab", "asm_Beng", "ast_Latn", "awa_Deva", "ayr_Latn", "azb_Arab", "azj_Latn", "bak_Cyrl", "bam_Latn", "ban_Latn", "bel_Cyrl", "bem_Latn", "ben_Beng", "bho_Deva", "bjn_Arab", "bjn_Latn", "bod_Tibt", "bos_Latn", "bug_Latn", "bul_Cyrl", "cat_Latn", "ceb_Latn", "ces_Latn", "cjk_Latn", "ckb_Arab", "crh_Latn", "cym_Latn", "dan_Latn", "deu_Latn", "dik_Latn", "dyu_Latn", "dzo_Tibt", "ell_Grek", "eng_Latn", "epo_Latn", "est_Latn", "eus_Latn", "ewe_Latn", "fao_Latn", "pes_Arab", "fij_Latn", "fin_Latn", "fon_Latn", "fra_Latn", "fur_Latn", "fuv_Latn", "gla_Latn", "gle_Latn", "glg_Latn", "grn_Latn", "guj_Gujr", "hat_Latn", "hau_Latn", "heb_Hebr", "hin_Deva", "hne_Deva", "hrv_Latn", "hun_Latn", "hye_Armn", "ibo_Latn", "ilo_Latn", "ind_Latn", "isl_Latn", "ita_Latn", "jav_Latn", "jpn_Jpan", "kab_Latn", "kac_Latn", "kam_Latn", "kan_Knda", "kas_Arab", "kas_Deva", "kat_Geor", "knc_Arab", "knc_Latn", "kaz_Cyrl", "kbp_Latn", "kea_Latn", "khm_Khmr", "kik_Latn", "kin_Latn", "kir_Cyrl", "kmb_Latn", "kon_Latn", "kor_Hang", "kmr_Latn", "lao_Laoo", "lvs_Latn", "lij_Latn", "lim_Latn", "lin_Latn", "lit_Latn", "lmo_Latn", "ltg_Latn", "ltz_Latn", "lua_Latn", "lug_Latn", "luo_Latn", "lus_Latn", "mag_Deva", "mai_Deva", "mal_Mlym", "mar_Deva", "min_Latn", "mkd_Cyrl", "plt_Latn", "mlt_Latn", "mni_Beng", "khk_Cyrl", "mos_Latn", "mri_Latn", "zsm_Latn", "mya_Mymr", "nld_Latn", "nno_Latn", "nob_Latn", "npi_Deva", "nso_Latn", "nus_Latn", "nya_Latn", "oci_Latn", "gaz_Latn", "ory_Orya", "pag_Latn", "pan_Guru", "pap_Latn", "pol_Latn", "por_Latn", "prs_Arab", "pbt_Arab", "quy_Latn", "ron_Latn", "run_Latn", "rus_Cyrl", "sag_Latn", "san_Deva", "sat_Beng", "scn_Latn", "shn_Mymr", "sin_Sinh", "slk_Latn", "slv_Latn", "smo_Latn", "sna_Latn", "snd_Arab", "som_Latn", "sot_Latn", "spa_Latn", "als_Latn", "srd_Latn", "srp_Cyrl", "ssw_Latn", "sun_Latn", "swe_Latn", "swh_Latn", "szl_Latn", "tam_Taml", "tat_Cyrl", "tel_Telu", "tgk_Cyrl", "tgl_Latn", "tha_Thai", "tir_Ethi", "taq_Latn", "taq_Tfng", "tpi_Latn", "tsn_Latn", "tso_Latn", "tuk_Latn", "tum_Latn", "tur_Latn", "twi_Latn", "tzm_Tfng", "uig_Arab", "ukr_Cyrl", "umb_Latn", "urd_Arab", "uzn_Latn", "vec_Latn", "vie_Latn", "war_Latn", "wol_Latn", "xho_Latn", "ydd_Hebr", "yor_Latn", "yue_Hant", "zho_Hans", "zho_Hant", "zul_Latn" ]})

if __name__ == "__main__":
    uvicorn.run("server:app", reload=True)
elif __name__ == 'server':
    print('loading model')
    device = 0 if torch.cuda.is_available() else -1
    device = -1
    model = AutoModelForSeq2SeqLM.from_pretrained(CKPT)
    tokenizer = AutoTokenizer.from_pretrained(CKPT)

app = FastAPI(
    docs_url='/',
    redoc_url=None,
)

cache = Path('cache')
cache.mkdir(exist_ok=True, parents=True)

def load_json(f):
    try:
        return json.loads(Path(f).read_text())
    except FileNotFoundError:
        return {}

def save_json(d, f):
    Path(f).write_text(json.dumps(d))

def translate(text, to, original):
    translation_pipeline = pipeline(TASK, model=model, tokenizer=tokenizer, src_lang=original, tgt_lang=to, max_length=MAX_LEN, device=device)
    result = translation_pipeline(text)
    translated_text = result[0]['translation_text']

    return translated_text

@app.post("/translate/text", response_class=PlainTextResponse)
def translate_text(
    text: str = Form("Glory to Ukraine! Glory to heroes!"),
    original: Languages = Form("eng_Latn"),
    to: Languages = Form("ukr_Cyrl"),
):
    f = f'cache/{text.replace("/","_")}'
    cache = load_json(f)
    if prop(to.value,cache):
        return cache[to.value]

    translation = translate(text, to.value, original.value)
    print({"to": to, "original": original, "text": text, "translation": translation})
    return translation

from pydantic import BaseModel, Field
class T(BaseModel):
    text: str = Form("download")
    original: str = Form("eng_Latn")
    to: List[Languages] = Form([Languages.eng_Latn, Languages.rus_Cyrl, Languages.azj_Latn])

@app.post("/translate/text2all")
def translate_text_to_all(t: T):
    t.text = to_lower(t.text)
    to = uniq(t.to)
    f = f'cache/{t.text.replace("/", "_")}'
    cache = load_json(f)
    for l in to:
        l = l.value
        if prop(l, cache):
            continue

        translation = to_lower(translate(t.text, l, t.original))
        cache[l] = translation
        save_json(cache, f)

    print(t.text, cache)
    return JSONResponse(cache)

@app.get('/translate/cache')
def get_all_cache():
    return from_pairs(map(lambda x: [replace('cache/', '', str(x)), load_json(x)], Path('cache').glob('*')))
