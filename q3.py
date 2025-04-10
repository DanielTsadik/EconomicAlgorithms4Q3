import pandas as pd
import numpy as np

# --- נתוני הקלט: שמות מפלגות, מספר הקולות שקיבלו, ותוצאות הבחירות המקוריות ---
data = {
    "Party": [
        "הליכוד", "יש עתיד", "הציונות הדתית", "המחנה הממלכתי", "ש\"ס",
        "יהדות התורה", "ישראל ביתנו", "רע\"מ", "חד\"ש תע\"ל", "העבודה"
    ],
    "Votes": [
        1115336, 847435, 516470, 432482, 392964,
        280194, 213687, 194047, 178735, 175992
    ],
    "Original_Seats": [32, 24, 14, 12, 11, 7, 6, 5, 5, 4]
}

# --- יצירת טבלת הנתונים הראשית (DataFrame) ---
df = pd.DataFrame(data)

# --- שלב 1: הקצאת מושב אחד ראשוני לכל מפלגה ---
df["Seats"] = 1  # כל מפלגה מתחילה עם מושב אחד
total_seats = 120  # סך המושבים בכנסת
initial_allocated = df["Seats"].sum()  # מושבים שהוקצו בתחילה (10)
remaining_seats = total_seats - initial_allocated  # כמה נשאר לחלק (110)

# --- פונקציית עדיפות לפי שיטת הנטינגטון-היל ---
def huntington_priority(votes, current_seats):
    denominator = np.sqrt(current_seats * (current_seats + 1))
    return votes / denominator

# --- שלב 2: הקצאת שאר המושבים אחד-אחד ---
for seat_round in range(remaining_seats):
    max_priority = -1
    party_to_allocate = None

    # נבדוק לכל מפלגה את העדיפות הנוכחית
    for index, row in df.iterrows():
        votes = row["Votes"]
        current_seats = row["Seats"]
        priority = huntington_priority(votes, current_seats)

        # נבחר את המפלגה עם העדיפות הגבוהה ביותר
        if priority > max_priority:
            max_priority = priority
            party_to_allocate = index

    # הוספת מושב למפלגה עם העדיפות הגבוהה ביותר
    df.at[party_to_allocate, "Seats"] += 1

# --- השוואת התוצאה מול הבחירות האמיתיות ---
df["Difference"] = df["Seats"] - df["Original_Seats"]

# --- הצגת התוצאות הסופיות, ממוינות לפי מספר מושבים בפועל ---
df_sorted = df.sort_values(by="Seats", ascending=False)
print(df_sorted[["Party", "Votes", "Original_Seats", "Seats", "Difference"]])