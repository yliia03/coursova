package hospital;

import java.util.HashMap;
import java.util.Map;

public class PlanTemplateRegistry {
    private final Map<String, TreatmentPlan> templates = new HashMap<>();

    public void register(String key, TreatmentPlan template) {
        templates.put(key, template.copy());
        Logger.log("Реєстр шаблонів", "Типовий план «" + key + "» збережено як прототип");
    }

    public TreatmentPlan createFor(String key, Patient patient) {
        TreatmentPlan template = templates.get(key);
        if (template == null) {
            throw new IllegalArgumentException("Невідомий типовий план: " + key);
        }
        TreatmentPlan plan = template.copy();
        plan.setPatientName(patient.getFullName());
        Logger.log("Реєстр шаблонів", "Створено копію типового плану «" + key + "» для " + patient);
        return plan;
    }

    public TreatmentPlan getTemplate(String key) {
        TreatmentPlan template = templates.get(key);
        return template == null ? null : template.copy();
    }
}
