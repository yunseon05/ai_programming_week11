
import pandas as pd


def 정제(df):
    print("시작:", len(df))

    # 1. 점수가 비어 있는 행 삭제
    df = df.dropna(subset=["점수"])
    print("빈 칸 제거:", len(df))

    # 2. 완전히 동일한 중복 행 제거
    df = df.drop_duplicates()
    print("중복 제거:", len(df))

    # 3. 반과 과목의 앞뒤 공백 제거
    df = df.copy()
    df["반"] = df["반"].str.strip()
    df["과목"] = df["과목"].str.strip()
    print("공백 제거:", len(df))

    # 4. 점수가 0~100 범위 밖인 행 삭제
    df = df[(df["점수"] >= 0) & (df["점수"] <= 100)]
    print("범위 밖 제거:", len(df))

    return df


# CSV 파일 불러오기
df = pd.read_csv("scores_2026.csv")

# 데이터 정제 실행
df = 정제(df)

math_df = df[df["과목"] == "수학"]
print("남은 행 수:", len(df))

# 반별 평균
print(df.groupby("반")["점수"].mean())

# 과목 × 반 평균
print(df.groupby(["과목", "반"])["점수"].mean())

# 반별 통계
print(df.groupby("반")["점수"].agg(
    개수="count",
    평균="mean",
    중앙값="median",
    최댓값="max"
).round(2))



# 1반과 2반 수학 스팟 체크
for class_name in ["1반", "2반"]:
    scores = df[(df["반"] == class_name) & (df["과목"] == "수학")]["점수"]

    print(f"\n{class_name} 수학 스팟 체크")
    print("점수 목록:", scores.tolist())
    print("학생 수:", len(scores))
    print("점수 합계:", scores.sum())
    print("평균:", scores.mean())



# mini.csv 손계산 검증
mini_df = pd.read_csv("mini.csv")
mini_df = 정제(mini_df)

print("정제 후 행 수:", len(mini_df))
print("반별 평균:")
print(mini_df.groupby("반")["점수"].mean())



def 반별평균(df):
    return df.groupby("반")["점수"].mean()
