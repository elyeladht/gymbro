CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);

CREATE TABLE exercises (
    exercise_id INTEGER PRIMARY KEY,
    exercise_name TEXT NOT NULL UNIQUE,
    exercise_description TEXT NOT NULL,
    targeted_muscles TEXT NOT NULL,
    is_machine INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE routines (
    routine_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    routine_name TEXT NOT NULL,
    routine_note TEXT,
    UNIQUE (user_id, routine_name),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE routine_exercises (
    routine_exercise_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    routine_id INTEGER NOT NULL,
    exercise_id INTEGER NOT NULL,
    target_sets INTEGER DEFAULT 3,
    target_reps INTEGER DEFAULT 10,
    target_weight REAL DEFAULT 0,
    UNIQUE (routine_id, exercise_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE 
    FOREIGN KEY (exercise_id) REFERENCES exercises(exercise_id) ON DELETE CASCADE
    FOREIGN KEY (routine_id) REFERENCES routines(routine_id) ON DELETE CASCADE
);

CREATE TABLE workout_log (
    log_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    exercise_id INTEGER NOT NULL,
    weight REAL NOT NULL,
    reps INTEGER NOT NULL,
    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES exercises(exercise_id)
);
