-- Trigger to check CGPA before inserting into Student table
CREATE OR REPLACE FUNCTION check_cgpa()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.cgpa > 10.0 THEN
        RAISE EXCEPTION 'CGPA cannot exceed 10.0';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_cgpa_trigger
BEFORE INSERT ON Student
FOR EACH ROW
EXECUTE FUNCTION check_cgpa();

-- Trigger to delete related records from other tables when a Faculty is deleted
CREATE OR REPLACE FUNCTION delete_faculty()
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM FacultyMobile WHERE fac_id = OLD.fac_id;
    DELETE FROM FacultyDepartment WHERE fac_id = OLD.fac_id;
    -- Add more delete statements as needed for other related tables
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER delete_faculty_trigger
AFTER DELETE ON Faculty
FOR EACH ROW
EXECUTE FUNCTION delete_faculty();



-- Trigger to delete related Enrollment records when a Course is deleted
CREATE OR REPLACE FUNCTION delete_enrollment_on_course_delete()
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM Enrollment WHERE course_id = OLD.course_id;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER delete_enrollment_on_course_delete_trigger
BEFORE DELETE ON Course
FOR EACH ROW
EXECUTE FUNCTION delete_enrollment_on_course_delete();

-- Trigger to delete related StudentAssignmentSubmission records when an Assignment is deleted
CREATE OR REPLACE FUNCTION delete_assignment_submission()
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM StudentAssignmentSubmission WHERE assignment_id = OLD.assignment_id;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER delete_assignment_submission_trigger
AFTER DELETE ON Assignment
FOR EACH ROW
EXECUTE FUNCTION delete_assignment_submission();


-- Trigger to update faculty joining date
CREATE OR REPLACE FUNCTION update_faculty_joining_date()
RETURNS TRIGGER AS $$
BEGIN
    NEW.joining_date := CURRENT_DATE;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_faculty_joining_date_trigger
BEFORE INSERT ON Faculty
FOR EACH ROW
EXECUTE FUNCTION update_faculty_joining_date();
