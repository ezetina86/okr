-- Clear existing data
TRUNCATE practices, okrs, key_results, actions, metrics CASCADE;

-- Insert practices
INSERT INTO practices (practice_id, name, owner) VALUES 
    (1, 'Cloud', 'Angelina Arreola'),
    (2, 'AT', 'Sergio Toscano'),
    (3, 'DEP', 'Diego Garcia'),
    (4, 'Testing', 'Bianca'),
    (5, 'DMO', 'Carlos Corona'),
    (6, 'Data', 'DI/DE'),
    (7, 'INOP', 'Claudio Espinoza');

-- Insert OKRs for each practice
INSERT INTO okrs (okr_id, practice_id, name, description, year, owner) 
SELECT 
    'OKR1_P' || p.practice_id, 
    p.practice_id,
    'People Engagement',
    'eNPS increase and employee retention',
    2025,
    'HR Lead'
FROM practices p
UNION ALL
SELECT 
    'OKR2_P' || p.practice_id,
    p.practice_id,
    'Operational Excellence',
    'Establish Mexico as a leading model for operational excellence',
    2025,
    'Operations Head'
FROM practices p
UNION ALL
SELECT 
    'OKR3_P' || p.practice_id,
    p.practice_id,
    'Delivery Excellence',
    'Establish Mexico as a leading model of delivery excellence',
    2025,
    'Delivery Head'
FROM practices p
UNION ALL
SELECT 
    'OKR4_P' || p.practice_id,
    p.practice_id,
    'Growing Business providing Integrated Solutions',
    'Enhance business growth through integrated solution offerings',
    2025,
    'Business Head'
FROM practices p
UNION ALL
SELECT 
    'OKR5_P' || p.practice_id,
    p.practice_id,
    'Proactive Innovation and Learning Improvement',
    'Improve Mexico contribution to Innovation and Learning',
    2025,
    'Learning Head'
FROM practices p;

-- Insert Key Results
INSERT INTO key_results (kr_id, okr_id, name, description, benchmark, target, current_value, status, tracking_frequency) VALUES 
    ('KR1.1', 'OKR1_P1', 'eNPS Improvement', 'eNPS increase from 71pts to 73pts (YoY)', 67, '≥67', 71, 'On Track', 'Quarterly'),
    ('KR1.2', 'OKR1_P1', 'EEI Maintenance', 'Maintain EEI at 91% or higher (YoY)', 90, '≥90', 91, 'On Track', 'Quarterly'),
    ('KR1.3', 'OKR1_P1', 'Attrition Control', 'Maintain voluntary attrition at 10.5% or lower', 0.109, '≤15%', 11, 'At Risk', 'Monthly'),
    ('KR2.1', 'OKR2_P1', 'Staffed Positions', 'Increase staffed positions from 65 to 100', 0.067, '≥20%', 18, 'At Risk', 'Monthly'),
    ('KR2.2', 'OKR2_P1', 'Bench Management', 'Maintain healthy bench below 8%', NULL, '≤6%', 5, 'On Track', 'Monthly'),
    ('KR3.1', 'OKR3_P1', 'EngX Education Program', 'Increase the EngX Education Program completion as per courses thresholds defined.', 0.5, '≤60%', 30, 'At Risk', 'Weekly'),
    ('KR3.2', 'OKR3_P1', 'EngX Experts certified', 'Increase the number of EngX Experts certified to X', 0, '3', 0, 'At Risk', 'Ongoing'),
    ('KR3.3', 'OKR3_P1', 'EngX Project Assessed', 'Increase # of EngX Project Assessed to X', 7, '10', 7, 'On Track', 'Ongoing'),
    ('KR3.4', 'OKR3_P1', 'POC Delivery', 'Deliver 1POC´s utilizing practice''s focus areas in Q1', 0, '1', 0, 'At Risk', 'Ongoing');

-- Insert Key Results for OKR4
INSERT INTO key_results (kr_id, okr_id, name, description, benchmark, target, current_value, status, tracking_frequency) VALUES 
    ('KR4.1', 'OKR4_P1', 'Capabilities Assessment', 'Current Capabilities assessment completed and definition of Integrated Solutions by Q1', 0, 100, 30, 'In Progress', 'Quarterly'),
    ('KR4.2', 'OKR4_P1', 'Pre-sales Training', 'All practice heads will Complete Pre-sales course by Q1', 0, 100, 0, 'Not Started', 'Quarterly'),
    ('KR4.3', 'OKR4_P1', 'RFP/RFI Tracking', 'Track participation in RFP/RFIs during Q1', 0, 100, 40, 'In Progress', 'Quarterly'),
    ('KR4.4', 'OKR4_P1', 'Market Presence', 'Foster EPAM MX presence and perception in the market', 0, 100, 25, 'In Progress', 'Ongoing');

-- Insert Key Results for OKR5
INSERT INTO key_results (kr_id, okr_id, name, description, benchmark, target, current_value, status, tracking_frequency) VALUES 
    ('KR5.1', 'OKR5_P1', 'English Proficiency', 'All B-tracks below C1 level scale up one English level', 0, 100, 0, 'Not Started', 'Quarterly'),
    ('KR5.2', 'OKR5_P1', 'AI Training', '70% of Mex resources will complete role specific AI knowledge training', 0, 70, 15, 'In Progress', 'Monthly'),
    ('KR5.3', 'OKR5_P1', 'Assessment Completion', 'Increase Assessment completion from 5% to 8%', 5, 8, 5, 'In Progress', 'Monthly');

-- Insert Actions
INSERT INTO actions (action_id, kr_id, description, owner, due_date, status) VALUES 
    ('A1.1.1', 'KR1.1', 'Continue with Quarterly town halls', 'Communications Manager', '2025-03-31', 'Complete'),
    ('A1.1.2', 'KR1.1', 'Monthly results alignment with RMs', 'Team Leaders', '2025-02-28', 'In Progress'),
    ('A1.2.1', 'KR1.2', 'Provide leadership development programs', 'L&D Manager', '2025-05-31', 'Not Started'),
    ('A1.2.2', 'KR1.2', 'Offer mentorship programs and career pathing', 'HR Team', '2025-04-30', 'In Progress'),
    ('A1.3.1', 'KR1.3', 'Establish early warning system', 'Analytics Team', '2025-03-15', 'Complete'),
    ('A1.3.2', 'KR1.3', 'Strengthen performance recognition programs', 'HR', '2025-06-30', 'Not Started'),
    ('A2.1.1', 'KR2.1', 'Implement targeted hiring strategies', 'Recruitment', '2025-03-31', 'In Progress'),
    ('A2.2.1', 'KR2.2', 'Enhance demand forecasting', 'Business Dev', '2025-04-15', 'In Progress'),
    ('A2.2.2', 'KR2.2', 'Launch training programs for market alignment', 'Training Team', '2025-05-31', 'Not Started'),
    ('A3.1.1', 'KR3.1', 'Increase the EngX Education Program completion', 'Training Team', '2025-05-31', 'Not Started'),
    ('A3.2.1', 'KR3.2', 'Identify one champion for each Unit in scope', 'Team Leaders', '2025-03-31', 'In Progress'),
    ('A3.2.2', 'KR3.2', 'Monitor and track completion', 'Delivery Manager', '2025-06-30', 'Not Started'),
    ('A3.4.1', 'KR3.4', 'Identify a relevant business problem aligned with practice focus areas', 'Delivery Manager', '2025-07-31', 'Not Started'),
    ('A3.4.2', 'KR3.4', 'Allocate resources and define clear objectives for the POC', 'Delivery Manager', '2025-08-31', 'Not Started'),
    ('A3.4.3', 'KR3.4', 'Execute and iterate based on feedback, ensuring tangible outcomes', 'Delivery Manager', '2025-05-31', 'Not Started');


-- Insert Actions for OKR4
INSERT INTO actions (action_id, kr_id, description, owner, due_date, status) VALUES 
    ('A4.1.1', 'KR4.1', 'Conduct a survey to assess current technical and delivery capabilities', 'Capability Lead', '2025-03-31', 'Not Started'),
    ('A4.1.2', 'KR4.1', 'Document and publish the finalized capabilities framework', 'Documentation Team', '2025-04-30', 'Not Started'),
    ('A4.1.3', 'KR4.1', 'Create and implement new deck/template for Capabilities showcase', 'Marketing Team', '2025-05-31', 'Not Started'),
    
    ('A4.2.1', 'KR4.2', 'Identify and enroll the required team for PreSales course', 'Training Coordinator', '2025-02-28', 'In Progress'),
    ('A4.2.2', 'KR4.2', 'Track and report completion rates', 'Training Coordinator', '2025-03-31', 'Not Started'),
    
    ('A4.3.1', 'KR4.3', 'Assign dedicated team members to monitor RFP/RFI opportunities', 'Sales Lead', '2025-02-15', 'Complete'),
    ('A4.3.2', 'KR4.3', 'Develop standardized response templates', 'Sales Team', '2025-03-15', 'In Progress'),
    ('A4.3.3', 'KR4.3', 'Conduct post-submission reviews', 'Sales Lead', '2025-03-31', 'Not Started'),
    
    ('A4.4.1', 'KR4.4', 'Engage in industry events and conferences', 'Marketing Team', '2025-12-31', 'In Progress'),
    ('A4.4.2', 'KR4.4', 'Enhance branding through case studies', 'Marketing Team', '2025-06-30', 'Not Started'),
    ('A4.4.3', 'KR4.4', 'Ensure sustained Green operations from Cloud', 'Operations Team', '2025-12-31', 'In Progress');

-- Insert Actions for OKR5
INSERT INTO actions (action_id, kr_id, description, owner, due_date, status) VALUES 
    ('A5.1.1', 'KR5.1', 'Organize structured language training sessions', 'L&D Team', '2025-06-30', 'Not Started'),
    ('A5.1.2', 'KR5.1', 'Implement periodic English proficiency assessments', 'L&D Team', '2025-12-31', 'Not Started'),
    
    ('A5.2.1', 'KR5.2', 'Implement AI learning paths on internal LMS', 'Training Team', '2025-03-31', 'In Progress'),
    ('A5.2.2', 'KR5.2', 'Recognize and reward AI training completion', 'HR Team', '2025-12-31', 'Not Started'),
    
    ('A5.3.1', 'KR5.3', 'Conduct targeted assessment preparation workshops', 'Training Team', '2025-04-30', 'Not Started'),
    ('A5.3.2', 'KR5.3', 'Provide Level-up materials for preparation', 'L&D Team', '2025-03-31', 'In Progress'),
    ('A5.3.3', 'KR5.3', 'Enable Pre-ASMT and peer mentoring programs', 'L&D Team', '2025-05-31', 'Not Started'),
    ('A5.3.4', 'KR5.3', 'Monitor and report assessment rates', 'Analytics Team', '2025-12-31', 'In Progress'),
    ('A5.3.5', 'KR5.3', 'Identify and address failure patterns', 'Analytics Team', '2025-12-31', 'Not Started');


-- Insert Metrics
INSERT INTO metrics (metric_id, kr_id, date, value, target, status) VALUES 
    ('M1.1_Q1', 'KR1.1', '2025-03-31', 71, 67, 'On Track'),
    ('M1.2_Q1', 'KR1.2', '2025-03-31', 91, 90, 'On Track'),
    ('M1.3_Jan', 'KR1.3', '2025-01-31', 10.8, 15, 'On Track'),
    ('M1.3_Feb', 'KR1.3', '2025-02-28', 11.2, 15, 'On Track'),  -- Changed from 02-29
    ('M2.1_Jan', 'KR2.1', '2025-01-31', 15, 20, 'At Risk'),
    ('M2.1_Feb', 'KR2.1', '2025-02-28', 18, 20, 'At Risk'),     -- Changed from 02-29
    ('M2.2_Jan', 'KR2.2', '2025-01-31', 6.1, 6, 'At Risk'),
    ('M2.2_Feb', 'KR2.2', '2025-02-28', 5.2, 6, 'On Track');    -- Changed from 02-29

-- Insert Metrics for new KRs
INSERT INTO metrics (metric_id, kr_id, date, value, target, status) VALUES 
    ('M4.1_Q1', 'KR4.1', '2025-03-31', 30, 100, 'In Progress'),
    ('M4.2_Q1', 'KR4.2', '2025-03-31', 0, 100, 'Not Started'),
    ('M4.3_Q1', 'KR4.3', '2025-03-31', 40, 100, 'In Progress'),
    ('M4.4_Q1', 'KR4.4', '2025-03-31', 25, 100, 'In Progress'),
    
    ('M5.1_Q1', 'KR5.1', '2025-03-31', 0, 100, 'Not Started'),
    ('M5.2_Jan', 'KR5.2', '2025-01-31', 15, 70, 'In Progress'),
    ('M5.2_Feb', 'KR5.2', '2025-02-28', 20, 70, 'In Progress'),
    ('M5.3_Jan', 'KR5.3', '2025-01-31', 5, 8, 'In Progress'),
    ('M5.3_Feb', 'KR5.3', '2025-02-28', 5.5, 8, 'In Progress');

    
-- Add verification queries
DO $$
BEGIN
    RAISE NOTICE 'Data verification:';
    RAISE NOTICE 'Practices count: %', (SELECT COUNT(*) FROM practices);
    RAISE NOTICE 'OKRs count: %', (SELECT COUNT(*) FROM okrs);
    RAISE NOTICE 'KRs count: %', (SELECT COUNT(*) FROM key_results);
    RAISE NOTICE 'Actions count: %', (SELECT COUNT(*) FROM actions);
    RAISE NOTICE 'Metrics count: %', (SELECT COUNT(*) FROM metrics);
END $$;

-- Add debug queries
SELECT 
    p.name as practice,
    o.name as okr_name,
    kr.kr_id,
    m.value,
    m.target,
    m.status
FROM practices p
JOIN okrs o ON p.practice_id = o.practice_id
LEFT JOIN key_results kr ON o.okr_id = kr.okr_id
LEFT JOIN metrics m ON kr.kr_id = m.kr_id
ORDER BY p.name, o.name, kr.kr_id;


-- Add this to your init_data.sql or run it separately
SELECT 
    o.name as okr_name,
    COUNT(DISTINCT kr.kr_id) as total_krs,
    SUM(CASE WHEN kr.status IN ('On Track', 'Complete') THEN 1 ELSE 0 END) as on_track_krs,
    SUM(CASE WHEN kr.status IN ('At Risk', 'Not Started', 'In Progress') THEN 1 ELSE 0 END) as at_risk_krs
FROM okrs o
LEFT JOIN key_results kr ON o.okr_id = kr.okr_id
GROUP BY o.name
ORDER BY o.name;