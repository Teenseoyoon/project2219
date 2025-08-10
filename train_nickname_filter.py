import fasttext

# 1. 학습 데이터 생성
clean_names = ["철수", "게임왕", "Sunshine123"]
offensive_names = ["욕설단어1", "욕설단어2", "offensiveword"]

with open("nickname_data.txt", "w", encoding="utf-8") as f:
    for name in clean_names:
        f.write(f"__label__clean {name}\n")
    for name in offensive_names:
        f.write(f"__label__offensive {name}\n")

print("✅ 학습 데이터 파일 생성 완료: nickname_data.txt")

# 2. fastText 모델 학습
model = fasttext.train_supervised(
    input="nickname_data.txt",
    lr=1.0,
    epoch=25,
    wordNgrams=2
)

# 3. 모델 저장
model.save_model("nickname_filter.bin")
print("✅ 모델 저장 완료: nickname_filter.bin")
