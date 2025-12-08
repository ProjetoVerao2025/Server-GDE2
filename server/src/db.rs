use axum::http::StatusCode;
use dotenv::dotenv;
use sqlx::postgres::PgPoolOptions;
use sqlx::Pool;
use sqlx::Postgres;
use sqlx::{Error, PgPool};
use std::env;

use crate::models::StudentLevel;
use crate::models::{Student, StudentLevel::Undergraduate};

pub struct DbResult<T> {
    pub error: String,
    pub message: String,
    pub result: T,
}

pub async fn prepare_db() -> Pool<Postgres> {
    let pool = connect_db().await;
    run_migrations(&pool);
    return pool;
}

async fn connect_db() -> Pool<Postgres> {
    dotenv().ok();

    let db_url = env::var("DB_URL").expect("Nao foi possivel obter a url do DB. Abortando\n");

    let pool = PgPoolOptions::new()
        .max_connections(5)
        .connect(&db_url)
        .await
        .expect("Nao foi possivel conectar ao banco de dados. Abortando.");

    return pool;
}

async fn run_migrations(pool: &PgPool) -> Result<(), sqlx::Error> {
    sqlx::migrate!("./migrations").run(pool).await?;
    Ok(())
}

pub async fn create_student(
    pool: &PgPool,
    ra: i32,
    name: String,
    program_code: i16,
    level: StudentLevel,
) -> DbResult<Student> {
    let result = sqlx::query_as::<_, Student>(
        "INSERT INTO students (ra, name, program_code, level) VALUES ($1, $2, $3, $4)",
    )
    .bind(&ra)
    .bind(name)
    .bind(program_code)
    .bind(level)
    .fetch_optional(pool)
    .await;
    match result {
        Ok(student) => {
            return DbResult {
                error: ("".to_string()),
                message: ("".to_string()),
                result: student.unwrap(),
            }
        }

        Err(Error::Database(db_err)) if db_err.code() == Some("23505".into()) => {
            eprint!("Erro {}\n", db_err);

            return DbResult {
                error: StatusCode::CONFLICT.to_string(),
                message: format!("A student with RA {} already exists", ra),
                result: Student {
                    ra: 0,
                    name: "".to_string(),
                    program_code: 0,
                    level: Undergraduate,
                },
            };
        }
        Err(err) => {
            eprintln!("Database error: {}", err);
            return DbResult {
                error: StatusCode::INTERNAL_SERVER_ERROR.to_string(),
                message: format!("Failed to create student: {}", err).to_string(),
                result: Student {
                    ra: 0,
                    name: "".to_string(),
                    program_code: 0,
                    level: Undergraduate,
                },
            };
        }
    }
}

pub async fn get_student_from_ra(pool: &PgPool, ra: i32) -> DbResult<Student> {
    let result = sqlx::query_as::<_, Student>("SELECT * FROM students WHERE ra=$1")
        .bind(&ra)
        .fetch_optional(pool)
        .await;
    match result {
        Ok(Some(student)) => {
            return DbResult {
                error: ("".to_string()),
                message: ("".to_string()),
                result: (student),
            }
        }

        Ok(None) => {
            return DbResult {
                error: "Student not found".to_string(),
                message: format!("There is no student with RA: {}", ra).to_string(),
                result: Student {
                    ra: 0,
                    name: "".to_string(),
                    program_code: 0,
                    level: Undergraduate,
                },
            };
        }

        Err(err) => {
            eprint!("Erro {}\n", err);

            return DbResult {
                error: StatusCode::INTERNAL_SERVER_ERROR.to_string(),
                message: format!("Failed to fetch student: {}", err),
                result: Student {
                    ra: 0,
                    name: "".to_string(),
                    program_code: 0,
                    level: Undergraduate,
                },
            };
        }
    }
}
