use crate::{db, models::Student};
use axum::{
    extract::{Path, State},
    http::StatusCode,
    response::IntoResponse,
    Json,
};

use serde::Serialize;
use sqlx::PgPool;

#[derive(Serialize)]
struct ErrorResponse {
    error: String,
    message: String,
}

pub async fn create_student(
    State(pool): State<PgPool>,
    Json(payload): Json<Student>,
) -> impl IntoResponse {
    let result = db::create_student(
        &pool,
        payload.ra,
        payload.name,
        payload.program_code,
        payload.level,
    )
    .await;
    if result.error == "".to_string() {
        return (StatusCode::OK, Json(result.result)).into_response();
    } else if result.error == StatusCode::CONFLICT.to_string() {
        let error = ErrorResponse {
            error: result.error,
            message: result.message,
        };
        return (StatusCode::CONFLICT, Json(error)).into_response();
    } else {
        return (
            StatusCode::INTERNAL_SERVER_ERROR,
            Json(ErrorResponse {
                error: result.error,
                message: result.message,
            }),
        )
            .into_response();
    }
}

pub async fn get_student(State(pool): State<PgPool>, Path(ra): Path<i32>) -> impl IntoResponse {
    let result = db::get_student_from_ra(&pool, ra).await;
    if result.error == "".to_string() {
        return (StatusCode::OK, Json(result.result)).into_response();
    } else if result.error == StatusCode::INTERNAL_SERVER_ERROR.to_string() {
        return (
            StatusCode::INTERNAL_SERVER_ERROR,
            Json(ErrorResponse {
                error: result.error,
                message: result.message,
            }),
        )
            .into_response();
    } else {
        return (
            StatusCode::NOT_FOUND,
            Json(ErrorResponse {
                error: result.error,
                message: result.message,
            }),
        )
            .into_response();
    }
}
