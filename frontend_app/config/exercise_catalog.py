"""
Aesthetic Physique Builder - Master Exercise Catalog & Split Architecture
Relative Path: frontend_app/config/exercise_catalog.py
Architectural Role: Complete dictionary of all 52 catalogued exercises,
unilateral pairings, equipment prerequisites, target execution modes,
and structured 7-day dual-session split definitions (Morning & Evening).
"""

from typing import Dict, List, Any, Optional

# ==============================================================================
# 1. Master Exercise Directory (All 52 Catalogued Exercises)
# ==============================================================================
EXERCISE_DIRECTORY: Dict[str, Dict[str, Any]] = {
    # --------------------------------------------------------------------------
    # Spinal Decompression & Upper Body A (Morning & Evening)
    # --------------------------------------------------------------------------
    "hang1": {
        "exercise_id": "hang1",
        "name": "Passive Bar Hang down (Dead Hang)",
        "category": "morning_decompression",
        "execution_mode": "timed_hold",
        "default_target_value": 45,
        "unilateral": False,
        "equipment_required": ["Pull-Up Bar"],
        "muscle_targets": ["Spine Decompression", "Forearms", "Lats"],
        "animation_asset": "hang1.gif",
        "rest_after_seconds": 60,
    },
    "hang2": {
        "exercise_id": "hang2",
        "name": "Passive Bar Hang up (Dead Hang)",
        "category": "morning_decompression",
        "execution_mode": "timed_hold",
        "default_target_value": 45,
        "unilateral": False,
        "equipment_required": ["Pull-Up Bar"],
        "muscle_targets": ["Spine Decompression", "Forearms", "Shoulders"],
        "animation_asset": "hang2.gif",
        "rest_after_seconds": 60,
    },
    "catcow": {
        "exercise_id": "catcow",
        "name": "Cat-Cow Stretch",
        "category": "morning_decompression",
        "execution_mode": "repetition_count",
        "default_target_value": 10,
        "unilateral": False,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Spine Mobility", "Core", "Neck"],
        "animation_asset": "catcow.gif",
        "rest_after_seconds": 30,
    },
    "cobra": {
        "exercise_id": "cobra",
        "name": "Cobra Pose (Bhujangasana)",
        "category": "morning_decompression",
        "execution_mode": "timed_hold",
        "default_target_value": 30,
        "unilateral": False,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Thoracic Extension", "Abdominals", "Chest"],
        "animation_asset": "cobra.gif",
        "rest_after_seconds": 30,
    },
    "toe_tuch": {
        "exercise_id": "toe_tuch",
        "name": "Standing Forward Fold (Toe Touch)",
        "category": "morning_decompression",
        "execution_mode": "timed_hold",
        "default_target_value": 30,
        "unilateral": False,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Hamstrings", "Lower Back", "Calves"],
        "animation_asset": "toe_tuch.gif",
        "rest_after_seconds": 30,
    },
    "wall": {
        "exercise_id": "wall",
        "name": "Wall Angle / Overhead Reach",
        "category": "morning_decompression",
        "execution_mode": "repetition_count",
        "default_target_value": 12,
        "unilateral": False,
        "equipment_required": ["None"],
        "muscle_targets": ["Shoulder Mobility", "Mid-Back", "Posture"],
        "animation_asset": "wall.gif",
        "rest_after_seconds": 30,
    },
    "jump": {
        "exercise_id": "jump",
        "name": "Maasai Jump",
        "category": "morning_decompression",
        "execution_mode": "repetition_count",
        "default_target_value": 20,
        "unilateral": False,
        "equipment_required": ["None"],
        "muscle_targets": ["Achilles Tendon", "Calves", "Bone Density"],
        "animation_asset": "jump.gif",
        "rest_after_seconds": 30,
    },
    "std_pushups": {
        "exercise_id": "std_pushups",
        "name": "Standard Floor Push-ups",
        "category": "evening_resistance",
        "execution_mode": "repetition_count",
        "default_target_value": 15,
        "target_notes": "2 reps before failure",
        "unilateral": False,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Pecs", "Triceps", "Anterior Delts"],
        "animation_asset": "std_pushups.gif",
        "rest_after_seconds": 90,
    },
    "bent_rows": {
        "exercise_id": "bent_rows",
        "name": "Bent-Over Dumbbell Rows",
        "category": "evening_resistance",
        "execution_mode": "repetition_count",
        "default_target_value": 15,
        "unilateral": False,
        "equipment_required": ["Dumbbells"],
        "muscle_targets": ["Lats", "Upper Back", "Rhomboids"],
        "animation_asset": "bent_rows.gif",
        "rest_after_seconds": 75,
    },
    "in_pushups": {
        "exercise_id": "in_pushups",
        "name": "Incline Push-Ups (Hands on bed/chair)",
        "category": "evening_resistance",
        "execution_mode": "repetition_count",
        "default_target_value": 15,
        "unilateral": False,
        "equipment_required": ["Chair"],
        "muscle_targets": ["Lower Chest", "Triceps"],
        "animation_asset": "in_pushups.gif",
        "rest_after_seconds": 60,
    },
    "overhead_triceps": {
        "exercise_id": "overhead_triceps",
        "name": "Overhead Dumbbell Triceps Extension",
        "category": "evening_resistance",
        "execution_mode": "repetition_count",
        "default_target_value": 15,
        "unilateral": False,
        "equipment_required": ["Dumbbells"],
        "muscle_targets": ["Triceps Long Head"],
        "animation_asset": "overhead_triceps.gif",
        "rest_after_seconds": 60,
    },
    "chair_dips": {
        "exercise_id": "chair_dips",
        "name": "Chair Dips",
        "category": "evening_resistance",
        "execution_mode": "repetition_count",
        "default_target_value": 12,
        "unilateral": False,
        "equipment_required": ["Chair"],
        "muscle_targets": ["Triceps", "Anterior Delts"],
        "animation_asset": "chair_dips.gif",
        "rest_after_seconds": 60,
    },
    "heel_touch": {
        "exercise_id": "heel_touch",
        "name": "Heel Touch",
        "category": "evening_resistance",
        "execution_mode": "repetition_count",
        "default_target_value": 15,
        "unilateral": False,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Obliques", "Core"],
        "animation_asset": "heel_touch.gif",
        "rest_after_seconds": 45,
    },

    # --------------------------------------------------------------------------
    # Hip Mobility & Lower Body A (Morning & Evening)
    # --------------------------------------------------------------------------
    "butterfly": {
        "exercise_id": "butterfly",
        "name": "Butterfly Stretch (Baddha Konasana)",
        "category": "flexibility",
        "execution_mode": "timed_hold",
        "default_target_value": 45,
        "unilateral": False,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Inner Adductors", "Groin"],
        "animation_asset": "butterfly.gif",
        "rest_after_seconds": 30,
    },
    "llstl": {
        "exercise_id": "llstl",
        "name": "Low Lunge Stretch Left (Anjaneyasana)",
        "category": "flexibility",
        "execution_mode": "timed_hold",
        "default_target_value": 30,
        "unilateral": True,
        "active_side": "LEFT",
        "paired_exercise_id": "llstr",
        "intra_set_rest_seconds": 20,
        "inter_set_rest_seconds": 30,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Hip Flexors", "Psoas"],
        "animation_asset": "llstl.gif",
        "rest_after_seconds": 20,
    },
    "llstr": {
        "exercise_id": "llstr",
        "name": "Low Lunge Stretch Right (Anjaneyasana)",
        "category": "flexibility",
        "execution_mode": "timed_hold",
        "default_target_value": 30,
        "unilateral": True,
        "active_side": "RIGHT",
        "paired_exercise_id": "llstl",
        "intra_set_rest_seconds": 20,
        "inter_set_rest_seconds": 30,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Hip Flexors", "Psoas"],
        "animation_asset": "llstr.gif",
        "rest_after_seconds": 30,
    },
    "hlsplit": {
        "exercise_id": "hlsplit",
        "name": "Half-Split Pose Left (Ardha Hanumanasana)",
        "category": "flexibility",
        "execution_mode": "timed_hold",
        "default_target_value": 30,
        "unilateral": True,
        "active_side": "LEFT",
        "paired_exercise_id": "hrsplit",
        "intra_set_rest_seconds": 20,
        "inter_set_rest_seconds": 30,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Hamstrings", "Calves"],
        "animation_asset": "hlsplit.gif",
        "rest_after_seconds": 20,
    },
    "hrsplit": {
        "exercise_id": "hrsplit",
        "name": "Half-Split Pose Right (Ardha Hanumanasana)",
        "category": "flexibility",
        "execution_mode": "timed_hold",
        "default_target_value": 30,
        "unilateral": True,
        "active_side": "RIGHT",
        "paired_exercise_id": "hlsplit",
        "intra_set_rest_seconds": 20,
        "inter_set_rest_seconds": 30,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Hamstrings", "Calves"],
        "animation_asset": "hrsplit.gif",
        "rest_after_seconds": 30,
    },
    "frog": {
        "exercise_id": "frog",
        "name": "Frog Pose (Mandukasana)",
        "category": "flexibility",
        "execution_mode": "timed_hold",
        "default_target_value": 45,
        "unilateral": False,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Adductors", "Hips", "Pelvis"],
        "animation_asset": "frog.gif",
        "rest_after_seconds": 45,
    },
    "ss_fold": {
        "exercise_id": "ss_fold",
        "name": "Seated Straddle Forward Fold",
        "category": "flexibility",
        "execution_mode": "timed_hold",
        "default_target_value": 30,
        "unilateral": False,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Hamstrings", "Groin", "Lower Back"],
        "animation_asset": "ss_fold.gif",
        "rest_after_seconds": 30,
    },
    "squatsl": {
        "exercise_id": "squatsl",
        "name": "Bulgarian Split Squats Left",
        "category": "evening_resistance",
        "execution_mode": "repetition_count",
        "default_target_value": 10,
        "unilateral": True,
        "active_side": "LEFT",
        "paired_exercise_id": "squatsr",
        "intra_set_rest_seconds": 20,
        "inter_set_rest_seconds": 120,
        "equipment_required": ["Dumbbells", "Chair"],
        "muscle_targets": ["Quads", "Glutes"],
        "animation_asset": "squatsl.gif",
        "rest_after_seconds": 20,
    },
    "squatsr": {
        "exercise_id": "squatsr",
        "name": "Bulgarian Split Squats Right",
        "category": "evening_resistance",
        "execution_mode": "repetition_count",
        "default_target_value": 10,
        "unilateral": True,
        "active_side": "RIGHT",
        "paired_exercise_id": "squatsl",
        "intra_set_rest_seconds": 20,
        "inter_set_rest_seconds": 120,
        "equipment_required": ["Dumbbells", "Chair"],
        "muscle_targets": ["Quads", "Glutes"],
        "animation_asset": "squatsr.gif",
        "rest_after_seconds": 120,
    },
    "squat": {
        "exercise_id": "squat",
        "name": "Goblet Squats",
        "category": "evening_resistance",
        "execution_mode": "repetition_count",
        "default_target_value": 15,
        "unilateral": False,
        "equipment_required": ["Dumbbells"],
        "muscle_targets": ["Quads", "Glutes", "Core"],
        "animation_asset": "squat.gif",
        "rest_after_seconds": 90,
    },
    "calfl": {
        "exercise_id": "calfl",
        "name": "Single-Leg Dumbbell Calf Raises Left",
        "category": "evening_resistance",
        "execution_mode": "repetition_count",
        "default_target_value": 15,
        "unilateral": True,
        "active_side": "LEFT",
        "paired_exercise_id": "calfr",
        "intra_set_rest_seconds": 5,
        "inter_set_rest_seconds": 60,
        "equipment_required": ["Dumbbells"],
        "muscle_targets": ["Gastrocnemius", "Soleus"],
        "animation_asset": "calfl.gif",
        "rest_after_seconds": 5,
    },
    "calfr": {
        "exercise_id": "calfr",
        "name": "Single-Leg Dumbbell Calf Raises Right",
        "category": "evening_resistance",
        "execution_mode": "repetition_count",
        "default_target_value": 15,
        "unilateral": True,
        "active_side": "RIGHT",
        "paired_exercise_id": "calfl",
        "intra_set_rest_seconds": 5,
        "inter_set_rest_seconds": 60,
        "equipment_required": ["Dumbbells"],
        "muscle_targets": ["Gastrocnemius", "Soleus"],
        "animation_asset": "calfr.gif",
        "rest_after_seconds": 60,
    },
    "leg_rises": {
        "exercise_id": "leg_rises",
        "name": "Lying Leg Raises",
        "category": "evening_resistance",
        "execution_mode": "repetition_count",
        "default_target_value": 15,
        "unilateral": False,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Lower Abs", "Hip Flexors"],
        "animation_asset": "leg_rises.gif",
        "rest_after_seconds": 60,
    },
    "plank": {
        "exercise_id": "plank",
        "name": "Forearm Plank",
        "category": "evening_resistance",
        "execution_mode": "timed_hold",
        "default_target_value": 60,
        "unilateral": False,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Transverse Abdominis", "Core", "Shoulders"],
        "animation_asset": "plank.gif",
        "rest_after_seconds": 60,
    },

    # --------------------------------------------------------------------------
    # Posture Alignment & Upper Body B (Morning & Evening)
    # --------------------------------------------------------------------------
    "rollover": {
        "exercise_id": "rollover",
        "name": "Pilates Roll-Over",
        "category": "morning_decompression",
        "execution_mode": "repetition_count",
        "default_target_value": 8,
        "unilateral": False,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Spine Articulation", "Hamstrings", "Core"],
        "animation_asset": "rollover.gif",
        "rest_after_seconds": 30,
    },
    "camel": {
        "exercise_id": "camel",
        "name": "Camel Pose (Ustrasana)",
        "category": "morning_decompression",
        "execution_mode": "timed_hold",
        "default_target_value": 20,
        "unilateral": False,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Thoracic Spine", "Chest", "Hip Flexors"],
        "animation_asset": "camel.gif",
        "rest_after_seconds": 30,
    },
    "down_dog": {
        "exercise_id": "down_dog",
        "name": "Downward-Facing Dog",
        "category": "morning_decompression",
        "execution_mode": "timed_hold",
        "default_target_value": 30,
        "unilateral": False,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Shoulder Stability", "Calves", "Hamstrings"],
        "animation_asset": "down_dog.gif",
        "rest_after_seconds": 30,
    },
    "glute": {
        "exercise_id": "glute",
        "name": "Glute Bridges",
        "category": "morning_decompression",
        "execution_mode": "timed_hold",
        "default_target_value": 30,
        "unilateral": False,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Glutes", "Hamstrings", "Pelvic Stability"],
        "animation_asset": "glute.gif",
        "rest_after_seconds": 30,
    },
    "d_pushups": {
        "exercise_id": "d_pushups",
        "name": "Decline Push-ups (Feet elevated on bed)",
        "category": "evening_resistance",
        "execution_mode": "repetition_count",
        "default_target_value": 12,
        "unilateral": False,
        "equipment_required": ["Chair"],
        "muscle_targets": ["Upper Chest (Clavicular Head)", "Triceps"],
        "animation_asset": "d_pushups.gif",
        "rest_after_seconds": 90,
    },
    "d_sh_press": {
        "exercise_id": "d_sh_press",
        "name": "Dumbbell Overhead Shoulder Press",
        "category": "evening_resistance",
        "execution_mode": "repetition_count",
        "default_target_value": 12,
        "unilateral": False,
        "equipment_required": ["Dumbbells"],
        "muscle_targets": ["Front Delts", "Side Delts", "Triceps"],
        "animation_asset": "d_sh_press.gif",
        "rest_after_seconds": 90,
    },
    "s_arm_row_l": {
        "exercise_id": "s_arm_row_l",
        "name": "Single-Arm Dumbbell Row Left (Braced on Bed)",
        "category": "evening_resistance",
        "execution_mode": "repetition_count",
        "default_target_value": 15,
        "unilateral": True,
        "active_side": "LEFT",
        "paired_exercise_id": "s_arm_row_r",
        "intra_set_rest_seconds": 5,
        "inter_set_rest_seconds": 60,
        "equipment_required": ["Dumbbells", "Exercise Bench"],
        "muscle_targets": ["Latissimus Dorsi", "Rhomboids"],
        "animation_asset": "s_arm_row_l.gif",
        "rest_after_seconds": 5,
    },
    "s_arm_row_r": {
        "exercise_id": "s_arm_row_r",
        "name": "Single-Arm Dumbbell Row Right (Braced on Bed)",
        "category": "evening_resistance",
        "execution_mode": "repetition_count",
        "default_target_value": 15,
        "unilateral": True,
        "active_side": "RIGHT",
        "paired_exercise_id": "s_arm_row_l",
        "intra_set_rest_seconds": 5,
        "inter_set_rest_seconds": 60,
        "equipment_required": ["Dumbbells", "Exercise Bench"],
        "muscle_targets": ["Latissimus Dorsi", "Rhomboids"],
        "animation_asset": "s_arm_row_r.gif",
        "rest_after_seconds": 60,
    },
    "d_l_raises": {
        "exercise_id": "d_l_raises",
        "name": "Dumbbell Lateral Raises",
        "category": "evening_resistance",
        "execution_mode": "repetition_count",
        "default_target_value": 15,
        "unilateral": False,
        "equipment_required": ["Dumbbells"],
        "muscle_targets": ["Lateral Delts (V-Taper Width)"],
        "animation_asset": "d_l_raises.gif",
        "rest_after_seconds": 60,
    },
    "re_snow_angles": {
        "exercise_id": "re_snow_angles",
        "name": "Reverse Snow Angels (Bodyweight)",
        "category": "evening_resistance",
        "execution_mode": "repetition_count",
        "default_target_value": 12,
        "unilateral": False,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Rear Delts", "Mid-Back", "Traps"],
        "animation_asset": "re_snow_angles.gif",
        "rest_after_seconds": 45,
    },
    "d_bi_curls": {
        "exercise_id": "d_bi_curls",
        "name": "Dumbbell Bicep Curls",
        "category": "evening_resistance",
        "execution_mode": "repetition_count",
        "default_target_value": 12,
        "unilateral": False,
        "equipment_required": ["Dumbbells"],
        "muscle_targets": ["Biceps Brachii", "Brachialis"],
        "animation_asset": "d_bi_curls.gif",
        "rest_after_seconds": 60,
    },
    "di_pushups": {
        "exercise_id": "di_pushups",
        "name": "Diamond Push-ups (Finisher)",
        "category": "evening_resistance",
        "execution_mode": "until_failure",
        "default_target_value": 15,
        "target_notes": "Until Failure",
        "unilateral": False,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Triceps", "Inner Pecs"],
        "animation_asset": "di_pushups.gif",
        "rest_after_seconds": 90,
    },

    # --------------------------------------------------------------------------
    # Yoga Flow & Lower Body B (Morning & Evening)
    # --------------------------------------------------------------------------
    "sun_salute": {
        "exercise_id": "sun_salute",
        "name": "Sun Salutations (Surya Namaskar)",
        "category": "yoga_flow",
        "execution_mode": "repetition_count",
        "default_target_value": 1,
        "unilateral": False,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Full Body Warm-Up", "Spine", "Hamstrings"],
        "animation_asset": "sun_salute.gif",
        "rest_after_seconds": 45,
    },
    "warrior_1_l": {
        "exercise_id": "warrior_1_l",
        "name": "Warrior I - Left (Virabhadrasana I)",
        "category": "yoga_flow",
        "execution_mode": "timed_hold",
        "default_target_value": 30,
        "unilateral": True,
        "active_side": "LEFT",
        "paired_exercise_id": "warrior_1_r",
        "intra_set_rest_seconds": 20,
        "inter_set_rest_seconds": 30,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Hip Flexors", "Quads", "Ankles"],
        "animation_asset": "warrior_1_l.gif",
        "rest_after_seconds": 20,
    },
    "warrior_1_r": {
        "exercise_id": "warrior_1_r",
        "name": "Warrior I - Right (Virabhadrasana I)",
        "category": "yoga_flow",
        "execution_mode": "timed_hold",
        "default_target_value": 30,
        "unilateral": True,
        "active_side": "RIGHT",
        "paired_exercise_id": "warrior_1_l",
        "intra_set_rest_seconds": 20,
        "inter_set_rest_seconds": 30,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Hip Flexors", "Quads", "Ankles"],
        "animation_asset": "warrior_1_r.gif",
        "rest_after_seconds": 30,
    },
    "warrior_2_l": {
        "exercise_id": "warrior_2_l",
        "name": "Warrior II - Left (Virabhadrasana II)",
        "category": "yoga_flow",
        "execution_mode": "timed_hold",
        "default_target_value": 30,
        "unilateral": True,
        "active_side": "LEFT",
        "paired_exercise_id": "warrior_2_r",
        "intra_set_rest_seconds": 20,
        "inter_set_rest_seconds": 30,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Groin", "Hips", "Chest"],
        "animation_asset": "warrior_2_l.gif",
        "rest_after_seconds": 20,
    },
    "warrior_2_r": {
        "exercise_id": "warrior_2_r",
        "name": "Warrior II - Right (Virabhadrasana II)",
        "category": "yoga_flow",
        "execution_mode": "timed_hold",
        "default_target_value": 30,
        "unilateral": True,
        "active_side": "RIGHT",
        "paired_exercise_id": "warrior_2_l",
        "intra_set_rest_seconds": 20,
        "inter_set_rest_seconds": 30,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Groin", "Hips", "Chest"],
        "animation_asset": "warrior_2_r.gif",
        "rest_after_seconds": 30,
    },
    "triagle_l_pose": {
        "exercise_id": "triagle_l_pose",
        "name": "Triangle Pose Left (Trikonasana)",
        "category": "yoga_flow",
        "execution_mode": "timed_hold",
        "default_target_value": 30,
        "unilateral": True,
        "active_side": "LEFT",
        "paired_exercise_id": "triagle_r_pose",
        "intra_set_rest_seconds": 20,
        "inter_set_rest_seconds": 30,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Hamstrings", "Groin", "Spine"],
        "animation_asset": "triagle_l_pose.gif",
        "rest_after_seconds": 20,
    },
    "triagle_r_pose": {
        "exercise_id": "triagle_r_pose",
        "name": "Triangle Pose Right (Trikonasana)",
        "category": "yoga_flow",
        "execution_mode": "timed_hold",
        "default_target_value": 30,
        "unilateral": True,
        "active_side": "RIGHT",
        "paired_exercise_id": "triagle_l_pose",
        "intra_set_rest_seconds": 20,
        "inter_set_rest_seconds": 30,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Hamstrings", "Groin", "Spine"],
        "animation_asset": "triagle_r_pose.gif",
        "rest_after_seconds": 30,
    },
    "child_pose": {
        "exercise_id": "child_pose",
        "name": "Child's Pose (Balasana)",
        "category": "yoga_flow",
        "execution_mode": "timed_hold",
        "default_target_value": 120,
        "unilateral": False,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Lower Back", "Hips", "Deep Breathing Recovery"],
        "animation_asset": "child_pose.gif",
        "rest_after_seconds": 0,
    },
    "dead_lifr": {
        "exercise_id": "dead_lifr",
        "name": "Dumbbell Romanian Deadlifts",
        "category": "evening_resistance",
        "execution_mode": "repetition_count",
        "default_target_value": 15,
        "unilateral": False,
        "equipment_required": ["Dumbbells"],
        "muscle_targets": ["Hamstrings", "Glutes", "Erector Spinae"],
        "animation_asset": "dead_lifr.gif",
        "rest_after_seconds": 90,
    },
    "walk_d": {
        "exercise_id": "walk_d",
        "name": "Walking Dumbbell Lunges",
        "category": "evening_resistance",
        "execution_mode": "repetition_count",
        "default_target_value": 20,
        "unilateral": False,
        "equipment_required": ["Dumbbells"],
        "muscle_targets": ["Quads", "Glutes", "Calves"],
        "animation_asset": "walk_d.gif",
        "rest_after_seconds": 90,
    },
    "ssquats": {
        "exercise_id": "ssquats",
        "name": "Sumo Squats",
        "category": "evening_resistance",
        "execution_mode": "repetition_count",
        "default_target_value": 15,
        "unilateral": False,
        "equipment_required": ["Dumbbells"],
        "muscle_targets": ["Inner Thighs (Adductors)", "Glutes"],
        "animation_asset": "ssquats.gif",
        "rest_after_seconds": 90,
    },
    "r_twists": {
        "exercise_id": "r_twists",
        "name": "Dumbbell Russian Twists",
        "category": "evening_resistance",
        "execution_mode": "repetition_count",
        "default_target_value": 20,
        "unilateral": False,
        "equipment_required": ["Dumbbells", "Mat"],
        "muscle_targets": ["Obliques", "Rotational Core"],
        "animation_asset": "r_twists.gif",
        "rest_after_seconds": 45,
    },
    "bi_crunch": {
        "exercise_id": "bi_crunch",
        "name": "Bicycle Crunches",
        "category": "evening_resistance",
        "execution_mode": "repetition_count",
        "default_target_value": 30,
        "unilateral": False,
        "equipment_required": ["Mat"],
        "muscle_targets": ["Rectus Abdominis", "Obliques"],
        "animation_asset": "bi_crunch.gif",
        "rest_after_seconds": 45,
    },
}

# ==============================================================================
# 2. Split Routines (Day A through Day G, Morning & Evening)
# ==============================================================================
ROUTINES: Dict[str, Dict[str, Any]] = {
    # --------------------------------------------------------------------------
    # DAY-A: Spinal Decompression & Upper Body A
    # --------------------------------------------------------------------------
    "DAY-A": {
        "title": "Spinal Decompression & Upper Body A",
        "morning": {
            "name": "Stretching & Posture (Spinal Decompression)",
            "expected_time_mins": 18,
            "exercises": [
                {"exercise_id": "hang1", "sets": 3, "target": 45, "rest_seconds": 60},
                {"exercise_id": "catcow", "sets": 2, "target": 10, "rest_seconds": 30},
                {"exercise_id": "cobra", "sets": 3, "target": 30, "rest_seconds": 30},
                {"exercise_id": "toe_tuch", "sets": 3, "target": 30, "rest_seconds": 30},
                {"exercise_id": "wall", "sets": 2, "target": 12, "rest_seconds": 30},
                {"exercise_id": "hang2", "sets": 3, "target": 45, "rest_seconds": 60},
                {"exercise_id": "jump", "sets": 2, "target": 20, "rest_seconds": 30},
            ]
        },
        "evening": {
            "name": "Upper Body A (Compound Press & Pull)",
            "expected_time_mins": 45,
            "exercises": [
                {"exercise_id": "std_pushups", "sets": 4, "target": 15, "rest_seconds": 90},
                {"exercise_id": "bent_rows", "sets": 4, "target": 15, "rest_seconds": 75},
                {"exercise_id": "d_sh_press", "sets": 3, "target": 12, "rest_seconds": 90},
                {"exercise_id": "in_pushups", "sets": 3, "target": 15, "rest_seconds": 60},
                {"exercise_id": "overhead_triceps", "sets": 3, "target": 15, "rest_seconds": 60},
                {"exercise_id": "chair_dips", "sets": 2, "target": 12, "rest_seconds": 60},
                {"exercise_id": "heel_touch", "sets": 2, "target": 15, "rest_seconds": 45},
            ]
        }
    },

    # --------------------------------------------------------------------------
    # DAY-B: Hip Mobility & Lower Body A
    # --------------------------------------------------------------------------
    "DAY-B": {
        "title": "Hip Mobility & Lower Body A",
        "morning": {
            "name": "Flexibility Training & Splits",
            "expected_time_mins": 20,
            "exercises": [
                {"exercise_id": "butterfly", "sets": 3, "target": 45, "rest_seconds": 30},
                {"exercise_id": "llstl", "sets": 3, "target": 30, "rest_seconds": 20},
                {"exercise_id": "llstr", "sets": 3, "target": 30, "rest_seconds": 30},
                {"exercise_id": "hlsplit", "sets": 3, "target": 30, "rest_seconds": 20},
                {"exercise_id": "hrsplit", "sets": 3, "target": 30, "rest_seconds": 30},
                {"exercise_id": "frog", "sets": 2, "target": 45, "rest_seconds": 45},
                {"exercise_id": "ss_fold", "sets": 3, "target": 30, "rest_seconds": 30},
            ]
        },
        "evening": {
            "name": "Lower Body A (Hypertrophy & Core)",
            "expected_time_mins": 48,
            "exercises": [
                {"exercise_id": "squatsl", "sets": 3, "target": 10, "rest_seconds": 20},
                {"exercise_id": "squatsr", "sets": 3, "target": 10, "rest_seconds": 120},
                {"exercise_id": "squat", "sets": 3, "target": 15, "rest_seconds": 90},
                {"exercise_id": "calfl", "sets": 4, "target": 15, "rest_seconds": 5},
                {"exercise_id": "calfr", "sets": 4, "target": 15, "rest_seconds": 60},
                {"exercise_id": "leg_rises", "sets": 3, "target": 15, "rest_seconds": 60},
                {"exercise_id": "plank", "sets": 3, "target": 60, "rest_seconds": 60},
            ]
        }
    },

    # --------------------------------------------------------------------------
    # DAY-C: Active Recovery / Mid-Week Rest
    # --------------------------------------------------------------------------
    "DAY-C": {
        "title": "Active Recovery / Mid-Week Rest",
        "morning": {
            "name": "Light Walk & Optional Decompression",
            "expected_time_mins": 20,
            "exercises": [
                {"exercise_id": "hang1", "sets": 2, "target": 45, "rest_seconds": 60},
                {"exercise_id": "catcow", "sets": 2, "target": 10, "rest_seconds": 30},
                {"exercise_id": "toe_tuch", "sets": 2, "target": 30, "rest_seconds": 30},
            ]
        },
        "evening": {
            "name": "Full Evening Rest (Muscle Tissue Repair)",
            "expected_time_mins": 0,
            "exercises": []
        }
    },

    # --------------------------------------------------------------------------
    # DAY-D: Posture Alignment & Upper Body B
    # --------------------------------------------------------------------------
    "DAY-D": {
        "title": "Posture Alignment & Upper Body B",
        "morning": {
            "name": "Posture Alignment & Spine Lengthening",
            "expected_time_mins": 20,
            "exercises": [
                {"exercise_id": "hang1", "sets": 3, "target": 45, "rest_seconds": 60},
                {"exercise_id": "rollover", "sets": 2, "target": 8, "rest_seconds": 30},
                {"exercise_id": "camel", "sets": 3, "target": 20, "rest_seconds": 30},
                {"exercise_id": "down_dog", "sets": 3, "target": 30, "rest_seconds": 30},
                {"exercise_id": "glute", "sets": 3, "target": 30, "rest_seconds": 30},
                {"exercise_id": "jump", "sets": 2, "target": 20, "rest_seconds": 30},
            ]
        },
        "evening": {
            "name": "Upper Body B (Shoulder Width & V-Taper)",
            "expected_time_mins": 50,
            "exercises": [
                {"exercise_id": "d_pushups", "sets": 4, "target": 12, "rest_seconds": 90},
                {"exercise_id": "s_arm_row_l", "sets": 4, "target": 15, "rest_seconds": 5},
                {"exercise_id": "s_arm_row_r", "sets": 4, "target": 15, "rest_seconds": 60},
                {"exercise_id": "d_l_raises", "sets": 4, "target": 15, "rest_seconds": 60},
                {"exercise_id": "re_snow_angles", "sets": 3, "target": 12, "rest_seconds": 45},
                {"exercise_id": "d_bi_curls", "sets": 4, "target": 12, "rest_seconds": 60},
                {"exercise_id": "di_pushups", "sets": 2, "target": 15, "rest_seconds": 90},
            ]
        }
    },

    # --------------------------------------------------------------------------
    # DAY-E: Yoga Flow & Lower Body B
    # --------------------------------------------------------------------------
    "DAY-E": {
        "title": "Yoga Flow & Lower Body B",
        "morning": {
            "name": "Yoga Flow & Balance Asanas",
            "expected_time_mins": 25,
            "exercises": [
                {"exercise_id": "sun_salute", "sets": 4, "target": 1, "rest_seconds": 45},
                {"exercise_id": "warrior_1_l", "sets": 2, "target": 30, "rest_seconds": 20},
                {"exercise_id": "warrior_1_r", "sets": 2, "target": 30, "rest_seconds": 30},
                {"exercise_id": "warrior_2_l", "sets": 2, "target": 30, "rest_seconds": 20},
                {"exercise_id": "warrior_2_r", "sets": 2, "target": 30, "rest_seconds": 30},
                {"exercise_id": "triagle_l_pose", "sets": 2, "target": 30, "rest_seconds": 20},
                {"exercise_id": "triagle_r_pose", "sets": 2, "target": 30, "rest_seconds": 30},
                {"exercise_id": "child_pose", "sets": 1, "target": 120, "rest_seconds": 0},
            ]
        },
        "evening": {
            "name": "Lower Body B (Posterior Chain & Core)",
            "expected_time_mins": 50,
            "exercises": [
                {"exercise_id": "dead_lifr", "sets": 4, "target": 15, "rest_seconds": 90},
                {"exercise_id": "walk_d", "sets": 3, "target": 20, "rest_seconds": 90},
                {"exercise_id": "ssquats", "sets": 3, "target": 15, "rest_seconds": 90},
                {"exercise_id": "calfl", "sets": 4, "target": 15, "rest_seconds": 5},
                {"exercise_id": "calfr", "sets": 4, "target": 15, "rest_seconds": 60},
                {"exercise_id": "r_twists", "sets": 3, "target": 20, "rest_seconds": 45},
                {"exercise_id": "bi_crunch", "sets": 3, "target": 30, "rest_seconds": 45},
            ]
        }
    },

    # --------------------------------------------------------------------------
    # DAY-F: Full Recovery
    # --------------------------------------------------------------------------
    "DAY-F": {
        "title": "Full Recovery & Muscle Synthesis",
        "morning": {
            "name": "Hydration, Nutrition & Rest",
            "expected_time_mins": 0,
            "exercises": []
        },
        "evening": {
            "name": "Full Rest (Protein Synthesis & Sleep)",
            "expected_time_mins": 0,
            "exercises": []
        }
    },

    # --------------------------------------------------------------------------
    # DAY-G: Full Recovery
    # --------------------------------------------------------------------------
    "DAY-G": {
        "title": "Full Recovery & Muscle Synthesis",
        "morning": {
            "name": "Rest & Habit Logging",
            "expected_time_mins": 0,
            "exercises": []
        },
        "evening": {
            "name": "Full Rest",
            "expected_time_mins": 0,
            "exercises": []
        }
    }
}

# ==============================================================================
# 3. Dynamic Helper Utilities
# ==============================================================================
def get_exercise_details(exercise_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves full metadata for an exercise by ID."""
    return EXERCISE_DIRECTORY.get(exercise_id)


def get_routine(day_id: str, session_type: str = "evening") -> Optional[Dict[str, Any]]:
    """Retrieves the routine definition for a given day (DAY-A through DAY-G)."""
    day_data = ROUTINES.get(day_id)
    if not day_data:
        return None
    session_key = session_type.lower()
    return day_data.get(session_key)


def get_routine_equipment(day_id: str, session_type: str = "evening") -> List[str]:
    """
    Parses all exercises in a designated routine and extracts a deduplicated list
    of physical equipment prerequisites for the Pre-Workout Requirements Shelf.
    """
    routine = get_routine(day_id, session_type)
    if not routine or not routine.get("exercises"):
        return ["None (Rest Day)"]

    equipment_set = set()
    for item in routine["exercises"]:
        ex_meta = EXERCISE_DIRECTORY.get(item["exercise_id"])
        if ex_meta:
            for eq in ex_meta.get("equipment_required", []):
                if eq and eq != "None":
                    equipment_set.add(eq)

    if not equipment_set:
        return ["Bodyweight Only (No Equipment)"]

    return sorted(list(equipment_set))
