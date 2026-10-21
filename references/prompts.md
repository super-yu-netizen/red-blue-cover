# 提示词模板

由助手根据当前内容填好变量。没有对应输入时删去该项，不把模板变成用户问卷。每张参考图按实际传入顺序说明用途。

## 新封面共用块

```text
Use case: ads-marketing.
Asset: a finished Chinese creator video cover, opaque PNG.
Topic and takeaway: [本期主题与一个准确利益点或悬念].
References: Image1 is the current user's authorized identity/expression/gesture reference. Image2 is red-blue style ONLY, never the identity or old text. Image3, if supplied, is the current real product/logo material.
Exact text: "[主标题第一行]" / "[主标题第二行]" / "[用户要求的小字或标签]".
Creator: preserve the person in Image1, including age, facial proportions, hairstyle, glasses if present, body and natural skin. Expression: [具体情绪]. Hands and pose: [每只手的位置、动作及与物件的接触].
Prop: [与当前主题结果相关的具体物件、所显示的真实或示意内容、自然比例].
Style: navy and dark crimson atmosphere; huge cream bold Chinese type with dark outline and dimensional shadow; gold emphasizes [一个重点]. Warm natural face light, restrained red/blue hair and edge light. Foreground/midground/background separated by perspective, occlusion, shadows and focus.
Accuracy: natural glyph proportions, correct hands and exact wording. No copied example brands, invented real screenshots, extra claims, unrelated English or watermark.
```

## 横版构图块

```text
Native landscape strict4:3 unless user explicitly requested another ratio. Independently arrange title, expressive face and foreground prop for this canvas. Use a diagonal reading path and clear visual hierarchy. Do not stretch a portrait image. No mandatory centered16:9 safe band, left3:4 title/logo area or empty top/bottom strips. Keep ordinary comfortable canvas margins.
```

## 竖版构图块

```text
Native portrait strict3:4 unless user explicitly requested another ratio. Design from top title to expressive creator to foreground prop. A two-row headline usually occupies the upper part; a concrete object and hands build depth below. Keep face and important words readable. Do not crop a landscape image into this layout or compress bodies/text.
```

百分比和位置按主题与字数调整，不把样图位置当作固定版式。共用块加当前画幅块后，直接调用可用图像工具，实际检查成品。

## 局部编辑

```text
Edit the attached finished cover. Change only [明确问题与区域] to exact "[替换文字或目标]".
Preserve the current person's identity, expression, pose, hands, prop, composition, red-blue lighting, texture and original canvas ratio, except the explicitly requested change.
Keep all other text verbatim. Correct punctuation spacing and preserve natural type proportions.
```

用户要求整体换主题或构图时，重新组织新图，不把局部编辑约束反过来限制明确请求。

