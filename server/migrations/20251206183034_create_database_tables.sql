-- Este arquivo cria a versão inicial das tabelas do banco de dados do sistema
-- Criado em 06/12/2025


-- Criando os enums necessários
CREATE TYPE student_level AS ENUM (
    'Undergraduate', -- Graduação
    'Graduate', -- Mestrado
    'Doctoral', -- Doutorado
    'Exchange', -- Intercambista
    'VisitingStudent' -- Estudante especial
    );


CREATE TYPE course_level AS ENUM (
    'Undergraduate',
    'Graduate'
    );


CREATE TYPE course_offering AS ENUM (
    'Odd',
    'Even',
    'Both',
    'None'
    );


CREATE TYPE weekday AS ENUM (
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday'
    );

CREATE TYPE attendance_status AS ENUM (
    'Present',
    'Absent',
    'Excused'
    );


-- Criando as tabelas


CREATE TABLE departments
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR(60)
);

CREATE TABLE courses
(
    id         SERIAL PRIMARY KEY,
    code       VARCHAR(6)      NOT NULL UNIQUE,
    name       VARCHAR(100)    NOT NULL,
    level      course_level,
    department INT             NOT NULL, -- ID do instituto que oferece a matéria
    credits    SMALLINT        NOT NULL,
    offered    course_offering NOT NULL,
    syllabus   TEXT,                     -- Ementa do curso.
    FOREIGN KEY (department) REFERENCES departments (id)
);

CREATE TABLE courseRequirements
(
    course_code      INT NOT NULL,
    requirement_code INT NOT NULL,
    PRIMARY KEY (course_code, requirement_code),
    FOREIGN KEY (course_code) REFERENCES courses (id),
    FOREIGN KEY (requirement_code) REFERENCES courses (id)
);

CREATE TABLE professors
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);



CREATE TABLE programs
(
    program_code  SMALLINT PRIMARY KEY     NOT NULL UNIQUE,
    program_name  VARCHAR(100) NOT NULL,
    department_id SMALLINT     NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments (id)
);

CREATE TABLE students
(
    ra           INT PRIMARY KEY NOT NULL,
    name         VARCHAR(100)    NOT NULL,
    program_code SMALLINT        NOT NULL, -- Código do curso do aluno. Exemplo (51) Cursao, (42) Ciência da comp.
    level        student_level   NOT NULL
);


CREATE TABLE classes
(
    id         SERIAL PRIMARY KEY,
    class_code INT     NOT NULL,
    letter     CHAR(1) NOT NULL,
    professor  INT     NOT NULL,
    FOREIGN KEY (class_code) REFERENCES courses (id),
    FOREIGN KEY (professor) REFERENCES professors (id)
);


CREATE TABLE attendances
(
    class_id   INT               NOT NULL,
    student_id INT               NOT NULL,
    signer_id  INT               NOT NULL,
    date       DATE              NOT NULL,
    status     attendance_status NOT NULL,
    PRIMARY KEY (class_id, student_id, date),
    FOREIGN KEY (class_id) REFERENCES classes (id) ON DELETE CASCADE,
    FOREIGN KEY (signer_id) REFERENCES students (ra),
    FOREIGN KEY (student_id) REFERENCES students (ra) ON DELETE CASCADE
);

CREATE TABLE enrollments
(
    student INT NOT NULL,
    class   INT NOT NULL,
    FOREIGN KEY (student) REFERENCES students (ra) ON DELETE CASCADE,
    FOREIGN KEY (class) REFERENCES classes (id) ON DELETE CASCADE
);

CREATE TABLE users
(
    id       INT          NOT NULL,
    password VARCHAR(100) NOT NULL,
    FOREIGN KEY (id) REFERENCES students (ra)
);
