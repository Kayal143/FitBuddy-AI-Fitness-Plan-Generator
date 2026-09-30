from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from uuid import uuid4

# --------------------------------------------------
# Project setup
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)

app = FastAPI(
    title="FitBuddy - AI Fitness Plan Generator"
)

users = {}


# --------------------------------------------------
# CREATE FITNESS PLAN
# --------------------------------------------------

def make_plan(goal, intensity):

    goal = str(goal).lower()
    intensity = str(intensity).lower()

    # ----------------------------
    # Weight Loss
    # ----------------------------

    if "weight" in goal or "loss" in goal:

        focus = "Calorie burning and full-body fitness"

        workouts = [
            "Brisk Walking - 30 minutes",
            "Bodyweight Squats - 3 sets x 12 reps",
            "Jumping Jacks - 3 sets x 20 reps",
            "Lunges - 3 sets x 10 reps",
            "Plank - 3 sets x 30 seconds",
            "Light Jogging - 25 minutes",
            "Stretching and Recovery"
        ]

    # ----------------------------
    # Muscle Gain
    # ----------------------------

    elif "muscle" in goal or "gain" in goal:

        focus = "Strength training and muscle building"

        workouts = [
            "Push-ups - 3 sets x 10 reps",
            "Bodyweight Squats - 3 sets x 15 reps",
            "Lunges - 3 sets x 10 reps",
            "Plank - 3 sets x 30 seconds",
            "Chair Dips - 3 sets x 10 reps",
            "Glute Bridges - 3 sets x 15 reps",
            "Full Body Stretching"
        ]

    # ----------------------------
    # Fitness
    # ----------------------------

    elif "fitness" in goal:

        focus = "Balanced fitness and endurance"

        workouts = [
            "Warm-up and Walking - 20 minutes",
            "Squats - 3 sets x 12 reps",
            "Push-ups - 3 sets x 10 reps",
            "Lunges - 3 sets x 10 reps",
            "Plank - 3 sets x 30 seconds",
            "Jogging - 20 minutes",
            "Stretching and Recovery"
        ]

    # ----------------------------
    # Default
    # ----------------------------

    else:

        focus = "General health and fitness"

        workouts = [
            "Walking - 20 minutes",
            "Squats - 3 sets x 10 reps",
            "Push-ups - 3 sets x 8 reps",
            "Lunges - 3 sets x 10 reps",
            "Plank - 3 sets x 20 seconds",
            "Light Jogging - 15 minutes",
            "Stretching and Recovery"
        ]

    # ----------------------------
    # Intensity adjustment
    # ----------------------------

    if "high" in intensity:

        workouts = [
            workout.replace("3 sets", "4 sets")
            for workout in workouts
        ]

    elif "low" in intensity:

        workouts = [
            workout.replace("3 sets", "2 sets")
            for workout in workouts
        ]

    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    weekly_plan = []

    for day, workout in zip(days, workouts):

        weekly_plan.append({
            "day": day,
            "workout": workout
        })

    return {
        "focus": focus,
        "weekly_plan": weekly_plan,
        "nutrition_tip": (
            "Drink enough water and eat balanced meals "
            "with fruits, vegetables and sufficient protein."
        ),
        "recovery_tip": (
            "Get 7-9 hours of sleep and give your body "
            "enough time to recover."
        )
    }


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# --------------------------------------------------
# GENERATE PLAN
# --------------------------------------------------

@app.post("/generate-workout", response_class=HTMLResponse)
async def generate_workout(request: Request):

    # Read all form data
    form = await request.form()

    # Print submitted data in terminal
    print("====================================")
    print("FORM DATA RECEIVED:")
    print(dict(form))
    print("====================================")

    # --------------------------------------------------
    # Accept different possible frontend field names
    # --------------------------------------------------

    name = (
        form.get("name")
        or form.get("username")
        or form.get("full_name")
        or "User"
    )

    age = (
        form.get("age")
        or form.get("user_age")
        or "20"
    )

    weight = (
        form.get("weight")
        or form.get("user_weight")
        or "60"
    )

    goal = (
        form.get("goal")
        or form.get("fitness_goal")
        or form.get("goal_type")
        or "General Fitness"
    )

    intensity = (
        form.get("intensity")
        or form.get("activity_level")
        or form.get("level")
        or "Medium"
    )

    # Convert age and weight safely
    try:
        age = int(age)
    except:
        age = 20

    try:
        weight = float(weight)
    except:
        weight = 60.0

    # --------------------------------------------------
    # Generate plan
    # --------------------------------------------------

    plan = make_plan(
        goal=goal,
        intensity=intensity
    )

    # --------------------------------------------------
    # User information
    # --------------------------------------------------

    user_data = {
        "id": str(uuid4()),
        "name": name,
        "age": age,
        "weight": weight,
        "goal": goal,
        "intensity": intensity
    }

    users[user_data["id"]] = user_data

    # Add user data to plan
    plan["user"] = user_data

    print("PLAN GENERATED SUCCESSFULLY")
    print(plan)

    # --------------------------------------------------
    # Show result page
    # --------------------------------------------------

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "plan": plan
        }
    )


# --------------------------------------------------
# UPDATE PLAN
# --------------------------------------------------

@app.post("/update-plan", response_class=HTMLResponse)
async def update_plan(request: Request):

    form = await request.form()

    print("UPDATE FORM DATA:")
    print(dict(form))

    name = form.get("name") or "User"
    age = form.get("age") or "20"
    weight = form.get("weight") or "60"
    goal = (
        form.get("goal")
        or form.get("fitness_goal")
        or "General Fitness"
    )
    intensity = (
        form.get("intensity")
        or form.get("activity_level")
        or "Medium"
    )

    try:
        age = int(age)
    except:
        age = 20

    try:
        weight = float(weight)
    except:
        weight = 60.0

    plan = make_plan(
        goal=goal,
        intensity=intensity
    )

    plan["user"] = {
        "name": name,
        "age": age,
        "weight": weight,
        "goal": goal,
        "intensity": intensity
    }

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "plan": plan
        }
    )


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
async def health():

    return {
        "status": "running",
        "message": "FitBuddy API is working"
    }