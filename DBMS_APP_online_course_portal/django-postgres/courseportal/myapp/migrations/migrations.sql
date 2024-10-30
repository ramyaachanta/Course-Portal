-- Define domains
CREATE DOMAIN password AS VARCHAR(20);
CREATE DOMAIN file AS VARCHAR(100);
CREATE DOMAIN credithours AS NUMERIC(5,0);
CREATE DOMAIN question AS VARCHAR(100);
CREATE DOMAIN ans AS VARCHAR(150);
CREATE DOMAIN Gender AS CHAR(1)
    CHECK (VALUE IN ('M', 'F', 'O'));

-- Create Department table
CREATE TABLE Department (
    department_name VARCHAR(50) PRIMARY KEY
);

-- Create Faculty table
CREATE TABLE Faculty (
    fac_id INTEGER PRIMARY KEY,
    password VARCHAR(20),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    DOB DATE,
    gender Gender,
    joining_date DATE
);

-- Create FacultyMobile table
CREATE TABLE FacultyMobile (
    mobile_no VARCHAR(20) PRIMARY KEY,
    fac_id INTEGER,
    CONSTRAINT fk_faculty_mobile_faculty FOREIGN KEY (fac_id) REFERENCES Faculty (fac_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create Course table
CREATE TABLE Course (
    course_id INTEGER PRIMARY KEY,
    course_name VARCHAR(100),
    credits DECIMAL(5),
    department_name VARCHAR(50) ,
    course_type VARCHAR(20),
    course_img VARCHAR(100),
    CONSTRAINT fk_course_dept FOREIGN KEY (department_name) REFERENCES Department (department_name) ON DELETE CASCADE ON UPDATE CASCADE

);

-- Create FacultyDepartment table
CREATE TABLE FacultyDepartment (
    fac_id INTEGER,
    department_name VARCHAR(50),
    PRIMARY KEY (fac_id, department_name),
    CONSTRAINT fk_faculty_department_faculty FOREIGN KEY (fac_id) REFERENCES Faculty (fac_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_faculty_department_department FOREIGN KEY (department_name) REFERENCES Department (department_name) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create Student table
CREATE TABLE Student (
    reg_no INTEGER PRIMARY KEY,
    password VARCHAR(20),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    dob DATE,
    cgpa FLOAT,
    year INTEGER,
    sem_no INTEGER,
    gender Gender
);

-- Create StudentDepartment table
CREATE TABLE StudentDepartment (
    reg_no INTEGER,
    department_name VARCHAR(50),
    PRIMARY KEY (reg_no, department_name),
    CONSTRAINT fk_student_department_student FOREIGN KEY (reg_no) REFERENCES Student (reg_no) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_student_department_department FOREIGN KEY (department_name) REFERENCES Department (department_name) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create StudentMobile table
CREATE TABLE StudentMobile (
    mobile_no VARCHAR(20) PRIMARY KEY,
    reg_no INTEGER ,
    CONSTRAINT fk_mobile_regno FOREIGN KEY (reg_no) REFERENCES Student (reg_no) ON DELETE CASCADE ON UPDATE CASCADE

);

-- Create Feedback table
CREATE TABLE Feedback (
    feedback_id VARCHAR(50) PRIMARY KEY,
    fac_id INTEGER,
    reg_no INTEGER,
    feedback_ans VARCHAR(150),
    feedback_question VARCHAR(100),
    date_submitted DATE,
    course_id INTEGER,
    CONSTRAINT fk_feedback_faculty FOREIGN KEY (fac_id) REFERENCES Faculty (fac_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_feedback_student FOREIGN KEY (reg_no) REFERENCES Student (reg_no) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_feedback_course FOREIGN KEY (course_id) REFERENCES Course (course_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create Assignment table
CREATE TABLE Assignment (
    assignment_id SERIAL PRIMARY KEY,
    title VARCHAR(100) DEFAULT '',
    total_marks FLOAT,
    message VARCHAR(500),
    assignment_file_question VARCHAR(100),
    end_time TIMESTAMP,
    start_time TIMESTAMP
);

-- Create AssignmentSubmission table
CREATE TABLE AssignmentSubmission (
    submission_id SERIAL PRIMARY KEY,
    message VARCHAR(500),
    assignment_file_answer VARCHAR(150),
    reg_no INTEGER ,
    assignment_id INTEGER ,
    CONSTRAINT fk_assignment_sub_regno FOREIGN KEY (reg_no) REFERENCES Student(reg_no) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_assignment_sub FOREIGN KEY (assignment_id) REFERENCES Assignment(assignment_id) ON DELETE CASCADE ON UPDATE CASCADE

);

-- Create FacultyAssignment table
CREATE TABLE FacultyAssignment (
    id SERIAL PRIMARY KEY,
    assignment_id INTEGER,
    fac_id INTEGER,
    course_id INTEGER,
    -- PRIMARY KEY (assignment_id, fac_id, course_id),
    CONSTRAINT fk_faculty_assignment_assignment FOREIGN KEY (assignment_id) REFERENCES Assignment (assignment_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_faculty_assignment_faculty FOREIGN KEY (fac_id) REFERENCES Faculty (fac_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_faculty_assignment_course FOREIGN KEY (course_id) REFERENCES Course (course_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create StudentAssignmentSubmission table
CREATE TABLE StudentAssignmentSubmission (
    id SERIAL,
    submission_id INTEGER,
    reg_no INTEGER,
    assignment_id INTEGER,
    marks FLOAT,
    PRIMARY KEY (id),
    CONSTRAINT fk_student_submission_assignment FOREIGN KEY (submission_id) REFERENCES AssignmentSubmission (submission_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_student_submission_student FOREIGN KEY (reg_no) REFERENCES Student (reg_no) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_student_submission_assignment_id FOREIGN KEY (assignment_id) REFERENCES Assignment (assignment_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create Enrollment table
CREATE TABLE Enrollment (
    id SERIAL PRIMARY KEY,
    course_id INTEGER,
    fac_id INTEGER,
    reg_no INTEGER,
    enrolled_on DATE,
    CONSTRAINT fk_enrollment_course FOREIGN KEY (course_id) REFERENCES Course (course_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_enrollment_faculty FOREIGN KEY (fac_id) REFERENCES Faculty (fac_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_enrollment_student FOREIGN KEY (reg_no) REFERENCES Student (reg_no) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create Materials table
CREATE TABLE Materials (
    material_id SERIAL PRIMARY KEY,
    material_file VARCHAR(100),
    material_title VARCHAR(100),
    course_id INTEGER ,
    description VARCHAR(200),
    CONSTRAINT fk_material_course FOREIGN KEY (course_id) REFERENCES Course (course_id) ON DELETE CASCADE ON UPDATE CASCADE

);

-- Create FacultyMaterial table
CREATE TABLE FacultyMaterial (
    id SERIAL PRIMARY KEY,
    fac_id INTEGER,
    material_id INTEGER,
    CONSTRAINT fk_faculty_material_faculty FOREIGN KEY (fac_id) REFERENCES Faculty (fac_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_faculty_material_material FOREIGN KEY (material_id) REFERENCES Materials (material_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create FAQ table
CREATE TABLE FAQ (
    faq_id SERIAL PRIMARY KEY,
    faq_qsn VARCHAR(100),
    faq_ans VARCHAR(150)
);

-- Create Announcements table
CREATE TABLE Announcements (
    publish_date DATE,
    notice_id SERIAL PRIMARY KEY,
    description VARCHAR(500),
    title VARCHAR(100)
);

-- Create FacultyAnnouncements table
CREATE TABLE FacultyAnnouncements (
    id SERIAL PRIMARY KEY,
    fac_id INTEGER,
    notice_id SERIAL ,
    course_id INTEGER ,
    -- PRIMARY KEY (fac_id, notice_id,course_id),
    CONSTRAINT fk_faculty_announcements_faculty FOREIGN KEY (fac_id) REFERENCES Faculty (fac_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_faculty_announcements_noticeid FOREIGN KEY (notice_id) REFERENCES Announcements(notice_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_faculty_announcements_course FOREIGN KEY(course_id) REFERENCES Course(course_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create StudentAnnouncements table
CREATE TABLE StudentAnnouncements (
    reg_no INTEGER,
    notice_id SERIAL,
    PRIMARY KEY (reg_no, notice_id),
    CONSTRAINT fk_student_announcements_student FOREIGN KEY (reg_no) REFERENCES Student (reg_no) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_student_announcements_noticeid FOREIGN KEY (notice_id) REFERENCES Announcements(notice_id) ON DELETE CASCADE ON UPDATE CASCADE

);

-- -- Create FacultyFAQ table
-- CREATE TABLE FacultyFAQ (
--     fac_id INTEGER,
--     faq_id SERIAL PRIMARY KEY,
--     CONSTRAINT fk_faculty_faq_faculty FOREIGN KEY (fac_id) REFERENCES Faculty (fac_id) ON DELETE CASCADE ON UPDATE CASCADE
-- );

-- -- Create StudentFAQ table
-- CREATE TABLE StudentFAQ (
--     reg_no INTEGER,
--     faq_id SERIAL PRIMARY KEY,
--     CONSTRAINT fk_student_faq_student FOREIGN KEY (reg_no) REFERENCES Student (reg_no) ON DELETE CASCADE ON UPDATE CASCADE
-- );
