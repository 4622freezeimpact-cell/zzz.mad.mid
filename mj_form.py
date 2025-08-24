import streamlit as st
import yaml

st.set_page_config(page_title="Midjourney YAML → Prompt 変換ツール", layout="centered")

st.title("🪄 Midjourney YAML → プロンプト変換ツール")

st.markdown(
    """
    このツールは、YAMLで書いたプロンプトをMidjourney用の1行プロンプトに変換します。  
    YAML形式のサンプルが下に入っていますので、編集して使ってください。
    """
)

# デフォルトのYAMLサンプル
default_yaml = """subject: エプロン姿で立つキャリアウーマン風な真面目な女子高生
setting:
  location: 朝食の準備に忙しい自宅のキッチン、キャベツを切っている女子高生、キッチンの窓から朝日が差し込んでいる
  time: ７月、午前７時
  lighting: 調理器具から強い反射光
style:
  art: グランブルーファンタジー風
  detail: 繊細な線と発色
  color: 濃いカラー
model:
  type: niji
parameters:
  aspect_ratio: 3:4
  stylize: 700
  chaos: 0
  seed: 42
notes: ガスコンロの上で湯気を出している鍋には昨日のカレー、ポットから沸騰のサイン
"""

yaml_text = st.text_area("✏️ YAML形式でプロンプトを入力：", value=default_yaml, height=300)

def yaml_to_prompt(yaml_text):
    try:
        data = yaml.safe_load(yaml_text)
        if not isinstance(data, dict):
            return "❌ YAMLの形式が正しくありません。"
    except Exception as e:
        return f"❌ YAML読み込みエラー: {e}"

    parts = []

    # subject
    if "subject" in data and data["subject"]:
        parts.append(str(data["subject"]))

    # setting
    if "setting" in data:
        for k, v in data["setting"].items():
            if v:
                parts.append(str(v))

    # style
    if "style" in data:
        for k, v in data["style"].items():
            if v:
                parts.append(str(v))

    # notes
    if "notes" in data and data["notes"]:
        parts.append(str(data["notes"]))

    # 本文プロンプト
    prompt = "、".join(parts)

    # parameters
    params = []
    if "model" in data and "type" in data["model"]:
        if data["model"]["type"] == "niji":
            params.append("--niji")
    if "parameters" in data:
        p = data["parameters"]
        if "aspect_ratio" in p: params.append(f"--ar {p['aspect_ratio']}")
        if "stylize" in p: params.append(f"--s {p['stylize']}")
        if "chaos" in p: params.append(f"--c {p['chaos']}")
        if "quality" in p: params.append(f"--q {p['quality']}")
        if "seed" in p: params.append(f"--seed {p['seed']}")

    return f"{prompt} {' '.join(params)}"

# 変換ボタン
if st.button("🔄 変換する"):
    result = yaml_to_prompt(yaml_text)
    st.subheader("✅ Midjourney用プロンプト")
    st.code(result, language="text")
    st.success("コピーしてMidjourneyに貼り付けてください！")
