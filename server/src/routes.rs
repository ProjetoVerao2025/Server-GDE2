use sqlx::PgPool;
use axum::{Router, routing::{get, post}};
use crate::handlers;

pub fn create_routes() -> Router<PgPool> {
    Router::new()
        .route("/students", post(handlers::create_student))
        .route("/students/:id", get(handlers::get_student))
}
