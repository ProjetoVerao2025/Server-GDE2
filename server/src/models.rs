// Esse arquivo define uma representacao de todos os objetos do nosso sistema.
// Aqui voce vai ter a definicao das estruturas de coisas como:
// Usuarios, Turmas, Professores, Horarios de oferecimento de materia ETC.

// Precisamos disso para poder converter nossos objetos para representacao em JSON
use serde::{Deserialize, Serialize};

// E disso para criar Tipos dentro do postgres
use sqlx::Type;

#[derive(Serialize, Deserialize, Type, Debug)]
#[sqlx(type_name = "student_level")]
pub enum StudentLevel {
    Undergraduate,   // Graduacao
    Graduate,        // Mestrado
    Doctoral,        // Doutorado
    Exchange,        // Intercabista
    VisitingStudent, // Estudante especial
}

// Se a diciplina e de nivel superior ou de graduacao.
#[derive(Serialize, Deserialize, Type, Debug)]
#[sqlx(type_name = "course_level")]
pub enum CourseLevel {
    Undergraduate,
    Graduate,
}

// Semestre de oferecimento da materia
#[derive(Serialize, Deserialize, Type, Debug)]
#[sqlx(type_name = "course_offering")]
pub enum CourseOffering {
    Odd,  // Primeiro Semestre / Semestre impar
    Even, // Segundo Semestre / Semestre par
    Both, // Oferecida nos dois semestre
    None, // Pode ser que a diciplina nao seja mais oferecida.
}

#[derive(Serialize, Deserialize, Type, Debug)]
#[sqlx(type_name = "weekday")]
pub enum WeekDay {
    Monday,
    Tuesday,
    Wednesday,
    Thursday,
    Friday,
    Saturday,
    Sunday,
}

// Status de presenca em aula
#[derive(Serialize, Deserialize, Type, Debug)]
#[sqlx(type_name = "attendance_status")]
pub enum AttendanceStatus {
    Present,
    Absent,
    Excused, // Abono de falta
}

// Estrutura basica que representa um "curso" ou materia da faculdade
#[derive(Serialize, Deserialize, sqlx::FromRow)]
pub struct Course {
    pub id: i32,
    pub code: String, // Nossa primary Key
    pub name: String,
    pub level: CourseLevel,
    pub department: i16, // ID do instituto que oferece a materia
    pub credits: i8,
    pub offered: CourseOffering,
    pub syllabus: String, // Ementa
}

// Instituto
pub struct Department {
    pub id: i16,
    pub name: String,
    pub acronym: String,
}

// Os requisitos de uma materia ficam em uma tabela propria, separada da materia em si
#[derive(Serialize, Deserialize, sqlx::FromRow)]
pub struct CourseRequirement {
    pub course_code: i32,
    pub requirement_code: i32,
}

// Nao sei o que colocar, mas por hora vai ficar assim so para garantir que nao vamos
// colocar professores que nao existem nas turmas.
#[derive(Serialize, Deserialize, sqlx::FromRow)]
pub struct Professor {
    pub id: i32, // Seria interessante usar o RA do professor, mas nao sei como conseguir isso.
    pub name: String,
}

// Equivalente a um curso de graduacao ou pos.
#[derive(Serialize, Deserialize, sqlx::FromRow)]
pub struct Program {
    pub id: i16,
    pub name: String,
}

#[derive(Serialize, Deserialize, sqlx::FromRow)]
pub struct Student {
    pub ra: i32, // Primary Key
    pub name: String,
    pub program_code: i16,   // Exemplo (42) Ciencia da Comp, (51) Cursao etc.
    pub level: StudentLevel, // Graduacao, Mestrado etc.
}

// Aqui sao as turmas de fato.
#[derive(Serialize, Deserialize, sqlx::FromRow)]
pub struct Class {
    pub id: i32,
    pub class_code: i32,
    pub letter: char, // Seria o Z em F158 (Z)
}

// Ausencia/Presenca em aula
#[derive(Serialize, Deserialize, sqlx::FromRow)]
pub struct Attendance {
    pub class_id: i32,
    pub student_id: i32,
    pub date: chrono::NaiveDate,
    pub status: AttendanceStatus,
}

// Matricula em discilplina
#[derive(Serialize, Deserialize, sqlx::FromRow)]
pub struct Enrollment {
    pub student: i32, // RA do aluno
    pub class_id: i32,
}
