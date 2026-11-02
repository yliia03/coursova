package hospital;

public class Bed {
    private final String wardNumber;
    private final String department;
    private BedState state = BedState.FREE;
    private Patient patient;

    public Bed(String wardNumber, String department) {
        this.wardNumber = wardNumber;
        this.department = department;
    }

    public String getWardNumber() {
        return wardNumber;
    }

    public String getDepartment() {
        return department;
    }

    public BedState getState() {
        return state;
    }

    public Patient getPatient() {
        return patient;
    }

    public boolean isFree() {
        return state == BedState.FREE;
    }

    void occupy(Patient p) {
        this.patient = p;
        this.state = BedState.OCCUPIED;
    }

    void release() {
        this.patient = null;
        this.state = BedState.FREE;
    }

    @Override
    public String toString() {
        return "ліжко " + wardNumber + " (" + department + ")";
    }
}
