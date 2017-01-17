INSERT INTO vtiger_crmentityrel
select DISTINCT
vtiger_targetscf.targetsid,
'Targets',
ee.crmid,
ee.setype
from 

vtiger_activity
JOIN vtiger_crmentity ea ON ea.crmid = vtiger_activity.activityid AND ea.deleted=0
JOIN vtiger_seactivityrel ON vtiger_seactivityrel.activityid = vtiger_activity.activityid
JOIN vtiger_crmentity ee ON ee.crmid = vtiger_seactivityrel.crmid AND ee.deleted=0
JOIN  vtiger_activitycf ON vtiger_activitycf.activityid = vtiger_activity.activityid
JOIN vtiger_targetscf on vtiger_targetscf.cf_1545 = vtiger_activitycf.cf_1547
JOIN vtiger_crmentity at ON at.crmid = vtiger_targetscf.targetsid AND at.deleted= 0
LEFT JOIN vtiger_crmentityrel ON vtiger_crmentityrel.crmid = at.crmid AND vtiger_crmentityrel.relmodule = ee.setype AND vtiger_crmentityrel.relcrmid = ee.crmid
WHERE vtiger_targetscf.cf_1545 IS NOT NULL AND vtiger_targetscf.cf_1545 <>''
AND vtiger_crmentityrel.crmid IS NULL