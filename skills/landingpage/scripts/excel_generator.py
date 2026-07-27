import argparse
import pandas as pd
from cursor_sdk import Cursor

ai = Cursor()


def ai_generate(product_info, column_name, lang):

    if lang == "zh":
        prompt = f"""
你是顶级众筹营销文案专家。

产品信息：
{product_info}

请根据产品信息生成【{column_name}】内容。

规则：

1. 大标题：≤10字
2. 副标题：≤15字

3. 生成6个卖点，每个卖点包含：
卖点标题
卖点说明

格式如下：

卖点标题
卖点说明

卖点标题
卖点说明

规则：

卖点标题 ≤10字
卖点说明 ≤20字
每个卖点占两行
先标题再说明

只输出文案
不要解释
"""
    else:
        prompt = f"""
You are a senior Kickstarter marketing copywriter.

Product information:
{product_info}

Generate content for column: {column_name}

Rules:

1. Headline ≤ 8 words
2. Subheadline ≤ 12 words

3. Generate 6 selling points

Format:

Title
Description

Title
Description

Rules:

Title ≤5 words
Description ≤12 words
Each selling point uses two lines

Output copy only.
No explanation.
"""

    result = ai.generate(prompt=prompt)

    return result.text.strip()


def read_product_info(path):

    df = pd.read_excel(path)

    text = ""

    for col in df.columns:
        text += f"{col}: {df[col].astype(str).str.cat(sep=' ')}\n"

    return text


def process_excel(input_file, template_file, output_file, lang):

    product_info = read_product_info(input_file)

    template_df = pd.read_excel(template_file)

    output_df = template_df.copy()

    for col in template_df.columns:

        if "卖点" in col or "headline" in col.lower() or "标题" in col:

            content = ai_generate(product_info, col, lang)

            lines = [l.strip() for l in content.split("\n") if l.strip()]

            if "卖点" in col:

                index = 0

                for i in range(6):

                    if index < len(lines):
                        output_df.at[0, f"卖点{i+1}"] = lines[index]
                        index += 1

                    if index < len(lines):
                        output_df.at[0, f"卖点{i+1}说明"] = lines[index]
                        index += 1

            else:

                if len(lines) > 0:
                    output_df.at[0, col] = lines[0]

    output_df.to_excel(output_file, index=False)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--input", required=True)
    parser.add_argument("--template", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--lang", default="zh")

    args = parser.parse_args()

    process_excel(
        args.input,
        args.template,
        args.output,
        args.lang
    )