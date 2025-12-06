use sqlx::{PgPool, Postgres, Pool};
use axum::{Router, routing::{get, post}, handler::Handler};
use crate::handlers;

pub fn create_routes() -> Router<PgPool> {
    Router::new()
        .route("./", get(handlers::teste))
        .route("/students", post(handlers::create_student))
        .route("/students/:id", get(handlers::get_student))
}
