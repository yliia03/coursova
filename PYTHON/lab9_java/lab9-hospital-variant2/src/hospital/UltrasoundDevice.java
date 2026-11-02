package hospital;

public class UltrasoundDevice {
    public static final String DEFAULT_PROFILE = "типовий";

    private final String id;
    private Patient currentPatient;
    private String settingsProfile = DEFAULT_PROFILE;

    public UltrasoundDevice(String id) {
        this.id = id;
        Logger.log("УЗД " + id, "Підключення та калібрування апарата...");
        Logger.work(600);
        Logger.log("УЗД " + id, "Апарат відкалібровано, готовий до роботи");
    }

    public String getId() {
        return id;
    }

    public Patient getCurrentPatient() {
        return currentPatient;
    }

    public String getSettingsProfile() {
        return settingsProfile;
    }

    void assign(Patient patient, String profile) {
        this.currentPatient = patient;
        this.settingsProfile = profile;
    }

    void reset() {
        this.currentPatient = null;
        this.settingsProfile = DEFAULT_PROFILE;
    }
}
