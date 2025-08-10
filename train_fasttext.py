import fasttext

model = fasttext.train_supervised(
    input="nickname_data.txt",
    lr=1.0,
    epoch=25,
    wordNgrams=2,
)
model.save_model("nickname_filter.bin")
print("모델 학습 완료 및 저장됨")
