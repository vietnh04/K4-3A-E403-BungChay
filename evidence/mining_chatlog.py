"""
Mining data/vlearn-pack/chatlog/tutor_turns.csv (repo de bai, KHONG commit data goc vao day).
Chay tu thu muc goc cua repo de bai (K4-3A-Day05-06-AI-Product-Hackathon-main), voi
CSV o duong dan data/vlearn-pack/chatlog/tutor_turns.csv.

Ket qua dung lam evidence chuan B cho spec.md SS1-SS2 (nhom BungChay, Track A1).
"""
import pandas as pd

CSV_PATH = "data/vlearn-pack/chatlog/tutor_turns.csv"


def main():
    df = pd.read_csv(CSV_PATH)

    real = df[df["is_preset"] == False]
    no_cite = real[real["has_citation"] == False]
    print(f"Cau hoi that (non-preset): {len(real)}/{len(df)}")
    print(f"Khong trich dan / cau hoi that: {len(no_cite)}/{len(real)} "
          f"= {len(no_cite) / len(real) * 100:.1f}%")

    k4 = df[df["cohort_hint"] == "K4"]
    k4_real = k4[k4["is_preset"] == False]
    k4_no_cite = k4_real[k4_real["has_citation"] == False]
    print(f"K4 - khong trich dan / cau hoi that: {len(k4_no_cite)}/{len(k4_real)} "
          f"= {len(k4_no_cite) / len(k4_real) * 100:.1f}%")

    print(f"ask_probing_question toan khoa: "
          f"{len(df[df['move_used'] == 'ask_probing_question'])}/{len(df)}")
    print(f"ask_probing_question K4: "
          f"{len(k4[k4['move_used'] == 'ask_probing_question'])}/{len(k4)}")


if __name__ == "__main__":
    main()
