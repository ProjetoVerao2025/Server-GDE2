use axum::{Json, extract::{Path, State}, response::IntoResponse, http::StatusCode};
use sqlx::PgPool;
use crate::models::Student;
use serde_json::{Value, json};


pub async fn create_student(
    State(pool): State<PgPool>,
    Json(payload): Json<Student>
) -> impl IntoResponse {
    let result = sqlx::query_as::<_, Student>(
        "INSERT INTO students (ra, name, program_code, level) VALUES ($1, $2, $3, $4) RETURNING *"
    )
        .bind(&payload.ra)
        .bind(&payload.name)
        .bind(&payload.program_code)
        .bind(&payload.level)
        .fetch_one(&pool)
        .await;

    match result {
        Ok(student) => (StatusCode::CREATED, Json(student)).into_response(),
        Err(err) => {
            // Log do erro do banco de dados para debug
            eprintln!("Database error: {}", err);

            (
                StatusCode::INTERNAL_SERVER_ERROR,
                // Retornando o erro para o cliente.
                format!("Failed to create student: {}", err)
            ).into_response()
        }
    }
}



pub async fn get_student(
    State(pool): State<PgPool>,
    Path(ra):  Path<i16>
) -> impl IntoResponse {

    let result = sqlx::query_as::<_, Student>(
        "SELECT name FROM students WHERE ra=$1"
    )
        .bind(&ra)
        .fetch_one(&pool)
        .await
        ;


    match result {
        Ok(student) => {
            (StatusCode::OK, Json(student)).into_response();
        }

        Err(err) => {
            eprint!("Erro {}\n", err);
        }
    }
}

