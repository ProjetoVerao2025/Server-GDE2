use axum::{Json, extract::{Path, State}, response::IntoResponse, http::StatusCode};
use sqlx::{PgPool, Error};
use crate::models::Student;
use serde::Serialize;



#[derive(Serialize)]
struct ErrorResponse {
    error: String,
    message: String,
}

pub async fn create_student(
    State(pool): State<PgPool>,
    Json(payload): Json<Student>
) -> impl IntoResponse {
    let result = sqlx::query_as::<_, Student>(
        "INSERT INTO students (ra, name, program_code, level) VALUES ($1, $2, $3, $4) RETURNING *"
    )
        .bind(&payload.ra) .bind(&payload.name)
        .bind(&payload.program_code)
        .bind(&payload.level)
        .fetch_one(&pool)
        .await;

    match result {
        Ok(student) => (StatusCode::CREATED, Json(student)).into_response(),


        Err(Error::Database(db_err)) if db_err.code() == Some("23505".into()) => {
            // Tentativa de criar usuario com RA já existente no banco de dados.
            let error = ErrorResponse {
                error: "Conflict".to_string(),
                message: format!("A student with RA {} already exists.", payload.ra),
            };

            (StatusCode::CONFLICT, Json(error)).into_response()
        }

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
    Path(ra):  Path<i32>
) -> impl IntoResponse {

    let result = sqlx::query_as::<_, Student>(
        "SELECT * FROM students WHERE ra=$1"
    )
        .bind(&ra)
        .fetch_optional(&pool)
        .await
        ;


    match result {
        Ok(Some(student)) => (StatusCode::OK, Json(student)).into_response(),


        Ok(None) => {
            let error_response = ErrorResponse {
                error: "Student not found".to_string(),
                message: format!("There is no student with RA: {}", ra).to_string()
            };

            ( StatusCode::OK, Json(error_response)).into_response() 
        }

        Err(err) => {
            eprint!("Erro {}\n", err);

            return (
                StatusCode::INTERNAL_SERVER_ERROR,
                format!("Failed to fetch student: {}", err)
            ).into_response();
        }
    }
}

