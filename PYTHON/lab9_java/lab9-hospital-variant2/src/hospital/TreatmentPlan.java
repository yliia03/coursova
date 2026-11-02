package hospital;

import java.util.ArrayList;
import java.util.List;

public class TreatmentPlan implements Prototype<TreatmentPlan> {
    private final String protocolName;
    private String patientName;
    private final List<String> analyses;
    private final List<String> procedures;
    private final List<String> prescriptions;
    private String diet;
    private String regime;

    private TreatmentPlan(String protocolName, List<String> analyses, List<String> procedures,
                          List<String> prescriptions, String diet, String regime) {
        this.protocolName = protocolName;
        this.analyses = analyses;
        this.procedures = procedures;
        this.prescriptions = prescriptions;
        this.diet = diet;
        this.regime = regime;
    }

    public static TreatmentPlan buildFromProtocol(String protocolName, List<String> analyses, List<String> procedures, List<String> prescriptions, String diet, String regime) {
        Logger.log("Конструктор планів", "Складання плану за протоколом «" + protocolName + "» (узгодження з клінічними рекомендаціями)...");
        Logger.work(300);
        return new TreatmentPlan(protocolName, new ArrayList<>(analyses), new ArrayList<>(procedures), new ArrayList<>(prescriptions), diet, regime);
    }

    @Override
    public TreatmentPlan copy() {
        TreatmentPlan clone = new TreatmentPlan(protocolName, new ArrayList<>(analyses), new ArrayList<>(procedures), new ArrayList<>(prescriptions), diet, regime);
        clone.patientName = this.patientName;
        return clone;
    }

    public String getProtocolName() {
        return protocolName;
    }

    public String getPatientName() {
        return patientName;
    }

    public void setPatientName(String patientName) {
        this.patientName = patientName;
    }

    public void addPrescription(String prescription) {
        prescriptions.add(prescription);
    }

    public boolean removePrescription(String prescription) {
        return prescriptions.remove(prescription);
    }

    public void setDiet(String diet) {
        this.diet = diet;
    }

    public void setRegime(String regime) {
        this.regime = regime;
    }

    public String describe() {
        return "план «" + protocolName + "»"  + (patientName != null ? " для " + patientName : " (типовий)") + ": аналізи=" + analyses + ", процедури=" + procedures  + ", призначення=" + prescriptions + ", дієта=" + diet + ", режим=" + regime;
    }
}
