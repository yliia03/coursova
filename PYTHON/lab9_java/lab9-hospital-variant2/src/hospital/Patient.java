package hospital;

public class Patient {
    private final String fullName;
    private String department;
    private String diagnosis;
    private final String attendingDoctor;

    public Patient(String fullName, String department, String diagnosis, String attendingDoctor) {
        this.fullName = fullName;
        this.department = department;
        this.diagnosis = diagnosis;
        this.attendingDoctor = attendingDoctor;
    }

    public String getFullName() {
        return fullName;
    }

    public String getDepartment() {
        return department;
    }

    public void setDepartment(String department) {
        this.department = department;
    }

    public String getDiagnosis() {
        return diagnosis;
    }

    public void setDiagnosis(String diagnosis) {
        this.diagnosis = diagnosis;
    }

    public String getAttendingDoctor() {
        return attendingDoctor;
    }

    @Override
    public String toString() {
        return fullName;
    }
}
