"""
Mining data/vlearn-pack/chatlog/tutor_turns.csv (repo de bai, KHONG commit data goc vao day).
Chay tu thu muc goc cua repo de bai (K4-3A-Day05-06-AI-Product-Hackathon-main), voi
CSV o duong dan data/vlearn-pack/chatlog/tutor_turns.csv.

Ket qua dung lam evidence chuan B cho spec.md SS1-SS2 (nhom BungChay, Track A2:
giang vien khong biet lop dang ket o dau).
"""
import pandas as pd

CSV_PATH = "data/vlearn-pack/chatlog/tutor_turns.csv"


def main():
    df = pd.read_csv(CSV_PATH)

    k4 = df[df["cohort_hint"] == "K4"]
    k4_real = k4[k4["is_preset"] == False]
    print(f"K4 - tong cau hoi that: {len(k4_real)}")

    by_lecture = (
        k4_real.groupby(["lecture_code", "lecture_title"])
        .agg(n_questions=("turn_id", "count"), n_students=("student", "nunique"))
        .sort_values("n_questions", ascending=False)
    )
    print("\nTop 5 bai giang co nhieu cau hoi that nhat (K4):")
    print(by_lecture.head(5))

    top = by_lecture.iloc[0]
    total = by_lecture["n_questions"].sum()
    print(f"\nBai giang '{by_lecture.index[0][1]}' ({by_lecture.index[0][0]}): "
          f"{top['n_questions']}/{total} cau hoi that "
          f"({top['n_questions'] / total * 100:.1f}%), tu {top['n_students']} hoc vien khac nhau")

    # review_concept = tutor phai on lai khai niem nen (dau hieu hoc vien dang ket)
    review = k4_real[k4_real["move_used"] == "review_concept"]
    by_lecture_review = (
        review.groupby(["lecture_code", "lecture_title"])["turn_id"]
        .count()
        .sort_values(ascending=False)
    )
    print(f"\nreview_concept / cau hoi that (K4): {len(review)}/{len(k4_real)} "
          f"= {len(review) / len(k4_real) * 100:.1f}%")
    print("\nTop 5 bai giang co nhieu luot 'review_concept' nhat (K4):")
    print(by_lecture_review.head(5))

    # 5 quote nguyen van tu bai giang co nhieu cau hoi/review_concept nhat
    top_code = by_lecture.index[0][0]
    quotes = k4_real[k4_real["lecture_code"] == top_code][
        ["turn_id", "student", "student_question", "move_used"]
    ].head(8)
    print(f"\nQuote mau tu bai giang '{top_code}':")
    for _, row in quotes.iterrows():
        print(f"[{row['turn_id']}] ({row['student']}, {row['move_used']}): {row['student_question'][:120]}")


if __name__ == "__main__":
    main()
