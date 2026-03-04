import React, { useState } from 'react';
import { 
  Layout, 
  Upload, 
  Button, 
  message, 
  Spin, 
  Typography, 
  Row, 
  Col,
  Input,
  Form,
  Progress,
  Tag,
  Divider,
  Alert,
  Space,
  Modal,
  Collapse
} from 'antd';
import { 
  InboxOutlined, 
  FileTextOutlined, 
  UserOutlined,
  PhoneOutlined,
  MailOutlined,
  TrophyOutlined,
  RobotOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  StarOutlined,
  BulbOutlined,
  BarChartOutlined,
  EnvironmentOutlined,
  EyeOutlined
} from '@ant-design/icons';
import axios from 'axios';
import './index.css';

const { Header, Content } = Layout;
const { Title, Text, Paragraph } = Typography;
const { Dragger } = Upload;
const { TextArea } = Input;
const { Panel } = Collapse;

// API配置
const API_BASE_URL = import.meta.env.PROD 
  ? 'https://api-lanxianlei.cn-hangzhou.fcapp.run' 
  : 'http://localhost:8000';

function App() {
  const [loading, setLoading] = useState(false);
  const [jobRequirement, setJobRequirement] = useState(null); // 岗位需求
  const [candidates, setCandidates] = useState([]); // 候选人列表
  const [selectedCandidate, setSelectedCandidate] = useState(null); // 选中的候选人
  const [detailModalVisible, setDetailModalVisible] = useState(false); // 详情弹窗
  const [pdfUrl, setPdfUrl] = useState(null); // PDF预览URL

  // 保存岗位需求
  const handleSaveJobRequirement = (values) => {
    setJobRequirement(values);
    message.success('✅ 岗位需求已保存，现在可以上传简历了！');
  };

  // 批量上传简历
  const handleBatchUpload = async (fileList) => {
    if (!jobRequirement) {
      message.error('请先填写岗位需求配置');
      return;
    }

    setLoading(true);
    const newCandidates = [];

    try {
      // 逐个上传并分析
      for (let i = 0; i < fileList.length; i++) {
        const file = fileList[i];
        
        try {
          // 创建PDF预览URL
          const pdfBlobUrl = URL.createObjectURL(file);
          
          // 1. 上传简历
          const formData = new FormData();
          formData.append('file', file);

          const uploadResponse = await axios.post(`${API_BASE_URL}/api/upload-resume`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
          });

          if (!uploadResponse.data.success) {
            message.error(`${file.name} 上传失败`);
            continue;
          }

          const resumeData = uploadResponse.data.data;

          // 2. 立即进行岗位匹配
          const matchResponse = await axios.post(`${API_BASE_URL}/api/match-job`, {
            resume_id: resumeData.resume_id,
            ...jobRequirement
          });

          if (matchResponse.data.success) {
            newCandidates.push({
              id: resumeData.resume_id,
              fileName: file.name,
              resumeInfo: resumeData.extracted_info,
              matchResult: matchResponse.data.data,
              uploadTime: new Date().toISOString(),
              pdfUrl: pdfBlobUrl // 保存PDF预览URL
            });
            message.success(`✅ ${file.name} 分析完成`);
          }
        } catch (error) {
          console.error(`Error processing ${file.name}:`, error);
          message.error(`${file.name} 处理失败`);
        }
      }

      // 按评分排序（从高到低）
      newCandidates.sort((a, b) => b.matchResult.total_score - a.matchResult.total_score);
      
      setCandidates(prev => {
        const combined = [...prev, ...newCandidates];
        combined.sort((a, b) => b.matchResult.total_score - a.matchResult.total_score);
        return combined;
      });
      
      message.success(`🎉 共分析 ${newCandidates.length} 份简历，已按匹配度排序`);
      
    } catch (error) {
      console.error('Batch upload error:', error);
      message.error('批量上传失败');
    } finally {
      setLoading(false);
    }
  };

  // 渲染欢迎区域
  const renderWelcomeSection = () => (
    <div className="welcome-section fade-in-up">
      <div style={{
        fontSize: '48px',
        fontWeight: 700,
        marginBottom: '16px',
        textShadow: '0 2px 8px rgba(0, 0, 0, 0.4)',
        color: '#ffffff',
        letterSpacing: '1px'
      }}>
        AI智能简历分析系统
      </div>
      <div style={{
        fontSize: '20px',
        marginBottom: '32px',
        fontWeight: 400,
        color: 'rgba(255, 255, 255, 0.95)',
        textShadow: '0 1px 4px rgba(0, 0, 0, 0.2)',
        lineHeight: 1.6
      }}>
        基于人工智能的简历解析与岗位匹配平台，支持批量分析，智能排序
      </div>
      <div className="feature-list">
        <div className="feature-item">
          <RobotOutlined className="feature-icon" />
          <span>AI智能解析</span>
        </div>
        <div className="feature-item">
          <BarChartOutlined className="feature-icon" />
          <span>批量处理</span>
        </div>
        <div className="feature-item">
          <BulbOutlined className="feature-icon" />
          <span>智能排序</span>
        </div>
        <div className="feature-item">
          <CheckCircleOutlined className="feature-icon" />
          <span>精准匹配</span>
        </div>
      </div>
    </div>
  );

  // 渲染候选人列表（按评分排序）
  const renderCandidatesList = () => {
    return (
      <div className="modern-card fade-in-up">
        <div className="card-header">
          <div className="card-title">
            <TrophyOutlined />
            候选人匹配排名
          </div>
          <div className="card-subtitle">
            共 {candidates.length} 位候选人，按AI评分从高到低排序
          </div>
        </div>
        
        <div style={{ padding: '0 24px 24px' }}>
          <Space direction="vertical" size="large" style={{ width: '100%' }}>
            {candidates.map((candidate, index) => {
              const { resumeInfo, matchResult, fileName } = candidate;
              const { basic_info, job_info, background } = resumeInfo;
              const { total_score, skill_match, experience_match, position_match, interview_suggestion } = matchResult;
              
              const getScoreColor = (score) => {
                if (score >= 80) return '#52c41a';
                if (score >= 60) return '#faad14';
                return '#ff4d4f';
              };

              const getRankBadge = (rank) => {
                if (rank === 0) return { icon: '🥇', color: '#ffd700', text: '最佳匹配' };
                if (rank === 1) return { icon: '🥈', color: '#c0c0c0', text: '次佳匹配' };
                if (rank === 2) return { icon: '🥉', color: '#cd7f32', text: '第三名' };
                return { icon: `#${rank + 1}`, color: '#1890ff', text: `第${rank + 1}名` };
              };

              const rankBadge = getRankBadge(index);

              // 生成AI评价
              const generateAIComment = () => {
                const comments = [];
                
                if (total_score >= 80) {
                  comments.push(`该候选人综合素质优秀，与岗位高度匹配。`);
                } else if (total_score >= 60) {
                  comments.push(`该候选人基本符合岗位要求。`);
                } else {
                  comments.push(`该候选人与岗位匹配度较低。`);
                }

                if (skill_match.score >= 80) {
                  comments.push(`技能方面表现突出，掌握了${skill_match.matched_skills?.length || 0}项关键技能。`);
                } else if (skill_match.score >= 60) {
                  comments.push(`具备部分所需技能，建议进一步评估。`);
                } else {
                  comments.push(`技能储备有待提升。`);
                }

                if (experience_match.score >= 80) {
                  comments.push(`工作经验丰富，符合岗位要求。`);
                } else if (experience_match.score >= 60) {
                  comments.push(`工作经验基本满足要求。`);
                }

                if (background.projects && background.projects.length >= 3) {
                  comments.push(`拥有${background.projects.length}个项目经验，实践能力较强。`);
                }

                return comments.join(' ');
              };

              return (
                <div 
                  key={candidate.id}
                  style={{
                    background: index < 3 
                      ? 'linear-gradient(135deg, #fff9e6 0%, #fff 100%)'
                      : 'white',
                    border: index === 0 
                      ? '2px solid #ffd700' 
                      : '1px solid #e8e8e8',
                    borderRadius: '16px',
                    padding: '24px',
                    paddingTop: '36px',
                    boxShadow: index === 0 
                      ? '0 8px 24px rgba(255, 215, 0, 0.2)'
                      : '0 2px 8px rgba(0,0,0,0.06)',
                    transition: 'all 0.3s ease',
                    position: 'relative',
                    cursor: 'pointer',
                    zIndex: 1
                  }}
                  onClick={() => {
                    setSelectedCandidate(candidate);
                    setDetailModalVisible(true);
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.transform = 'translateY(-4px)';
                    e.currentTarget.style.boxShadow = '0 12px 32px rgba(0,0,0,0.12)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = 'translateY(0)';
                    e.currentTarget.style.boxShadow = index === 0 
                      ? '0 8px 24px rgba(255, 215, 0, 0.2)'
                      : '0 2px 8px rgba(0,0,0,0.06)';
                  }}
                >
                  {/* 排名标识 */}
                  <div style={{
                    position: 'absolute',
                    top: '-12px',
                    left: '24px',
                    background: rankBadge.color,
                    color: 'white',
                    padding: '6px 16px',
                    borderRadius: '20px',
                    fontSize: '14px',
                    fontWeight: 'bold',
                    boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
                    zIndex: 10
                  }}>
                    {rankBadge.icon} {rankBadge.text}
                  </div>

                  {/* 操作按钮组 */}
                  <div style={{
                    position: 'absolute',
                    top: '20px',
                    right: '24px',
                    display: 'flex',
                    gap: '8px',
                    zIndex: 10
                  }}>
                    {candidate.pdfUrl && (
                      <div 
                        style={{
                          background: '#52c41a',
                          color: 'white',
                          padding: '8px 16px',
                          borderRadius: '8px',
                          fontSize: '12px',
                          fontWeight: 'bold',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '6px',
                          cursor: 'pointer'
                        }}
                        onClick={(e) => {
                          e.stopPropagation();
                          window.open(candidate.pdfUrl, '_blank');
                        }}
                      >
                        <FileTextOutlined />
                        查看PDF
                      </div>
                    )}
                    <div style={{
                      background: '#1890ff',
                      color: 'white',
                      padding: '8px 16px',
                      borderRadius: '8px',
                      fontSize: '12px',
                      fontWeight: 'bold',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '6px'
                    }}>
                      <EyeOutlined />
                      查看详情
                    </div>
                  </div>

                  <Row gutter={[24, 24]} style={{ marginTop: '12px' }}>
                    {/* 左侧：候选人信息 */}
                    <Col xs={24} lg={14}>
                      <div style={{ marginBottom: '16px' }}>
                        <Text strong style={{ fontSize: '18px', color: '#2c3e50' }}>
                          <UserOutlined style={{ marginRight: 8 }} />
                          {basic_info.name || '未识别姓名'}
                        </Text>
                        <Tag color="blue" style={{ marginLeft: 12 }}>
                          {fileName}
                        </Tag>
                      </div>

                      <Space direction="vertical" size="small" style={{ width: '100%' }}>
                        <div>
                          <PhoneOutlined style={{ marginRight: 8, color: '#1890ff' }} />
                          <Text>{basic_info.phone || '未提供'}</Text>
                        </div>
                        <div>
                          <MailOutlined style={{ marginRight: 8, color: '#52c41a' }} />
                          <Text>{basic_info.email || '未提供'}</Text>
                        </div>
                        <div>
                          <FileTextOutlined style={{ marginRight: 8, color: '#722ed1' }} />
                          <Text strong>目标职位：</Text>
                          <Tag color="purple">{job_info.position || '未明确'}</Tag>
                        </div>
                        <div>
                          <ClockCircleOutlined style={{ marginRight: 8, color: '#fa8c16' }} />
                          <Text strong>工作经验：</Text>
                          <Tag color="orange">{background.work_years || '未明确'}</Tag>
                        </div>
                        <div>
                          <StarOutlined style={{ marginRight: 8, color: '#faad14' }} />
                          <Text strong>学历：</Text>
                          <Tag color="gold">{background.education || '未明确'}</Tag>
                        </div>
                      </Space>

                      {/* 技能标签 */}
                      {background.skills && background.skills.length > 0 && (
                        <div style={{ marginTop: '16px' }}>
                          <Text strong style={{ display: 'block', marginBottom: '8px' }}>
                            专业技能：
                          </Text>
                          <div>
                            {background.skills.slice(0, 6).map((skill, idx) => (
                              <Tag key={idx} color="blue" style={{ marginBottom: 4 }}>
                                {skill}
                              </Tag>
                            ))}
                            {background.skills.length > 6 && (
                              <Tag>+{background.skills.length - 6}项</Tag>
                            )}
                          </div>
                        </div>
                      )}

                      {/* AI评价 */}
                      <div style={{
                        marginTop: '16px',
                        padding: '12px',
                        background: 'linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%)',
                        borderRadius: '8px',
                        borderLeft: '3px solid #4caf50'
                      }}>
                        <div style={{ marginBottom: '6px' }}>
                          <RobotOutlined style={{ color: '#4caf50', marginRight: 6 }} />
                          <Text strong style={{ color: '#2e7d32' }}>AI综合评价</Text>
                        </div>
                        <Paragraph 
                          style={{ 
                            margin: 0, 
                            fontSize: '13px', 
                            color: '#33691e',
                            lineHeight: 1.6
                          }}
                        >
                          {generateAIComment()}
                        </Paragraph>
                      </div>
                    </Col>

                    {/* 右侧：匹配评分 */}
                    <Col xs={24} lg={10}>
                      <div style={{
                        background: 'linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%)',
                        padding: '20px',
                        borderRadius: '12px',
                        border: '2px solid #bae7ff',
                        textAlign: 'center'
                      }}>
                        <div style={{
                          fontSize: '48px',
                          fontWeight: 'bold',
                          color: getScoreColor(total_score),
                          marginBottom: '8px'
                        }}>
                          {total_score}分
                        </div>
                        <Text type="secondary">综合匹配度</Text>

                        <Divider style={{ margin: '16px 0' }} />

                        <Space direction="vertical" size="small" style={{ width: '100%' }}>
                          <div style={{ textAlign: 'left' }}>
                            <Text style={{ fontSize: '12px' }}>技能匹配</Text>
                            <Progress 
                              percent={skill_match.score} 
                              strokeColor={getScoreColor(skill_match.score)}
                              size="small"
                            />
                          </div>
                          <div style={{ textAlign: 'left' }}>
                            <Text style={{ fontSize: '12px' }}>经验匹配</Text>
                            <Progress 
                              percent={experience_match.score} 
                              strokeColor={getScoreColor(experience_match.score)}
                              size="small"
                            />
                          </div>
                          <div style={{ textAlign: 'left' }}>
                            <Text style={{ fontSize: '12px' }}>职位匹配</Text>
                            <Progress 
                              percent={position_match.score} 
                              strokeColor={getScoreColor(position_match.score)}
                              size="small"
                            />
                          </div>
                        </Space>

                        <Divider style={{ margin: '16px 0' }} />

                        {total_score >= 80 ? (
                          <Alert
                            message="强烈推荐面试"
                            type="success"
                            showIcon
                            style={{ fontSize: '12px' }}
                          />
                        ) : total_score >= 60 ? (
                          <Alert
                            message="建议面试"
                            type="warning"
                            showIcon
                            style={{ fontSize: '12px' }}
                          />
                        ) : (
                          <Alert
                            message="暂不推荐"
                            type="error"
                            showIcon
                            style={{ fontSize: '12px' }}
                          />
                        )}
                      </div>
                    </Col>
                  </Row>
                </div>
              );
            })}
          </Space>
        </div>
      </div>
    );
  };

  // 渲染候选人详情弹窗
  const renderDetailModal = () => {
    if (!selectedCandidate) return null;

    const { resumeInfo, matchResult, fileName, pdfUrl } = selectedCandidate;
    const { basic_info, job_info, background } = resumeInfo;
    const { total_score, skill_match, experience_match, position_match, recommendations } = matchResult;

    const getScoreColor = (score) => {
      if (score >= 80) return '#52c41a';
      if (score >= 60) return '#faad14';
      return '#ff4d4f';
    };

    return (
      <Modal
        title={
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <UserOutlined style={{ fontSize: '24px', color: '#1890ff' }} />
              <div>
                <div style={{ fontSize: '18px', fontWeight: 'bold' }}>
                  {basic_info.name || '未识别姓名'}
                </div>
                <Text type="secondary" style={{ fontSize: '12px' }}>
                  {fileName}
                </Text>
              </div>
            </div>
            {pdfUrl && (
              <Button 
                type="primary" 
                icon={<FileTextOutlined />}
                onClick={() => window.open(pdfUrl, '_blank')}
              >
                查看原始PDF
              </Button>
            )}
          </div>
        }
        open={detailModalVisible}
        onCancel={() => setDetailModalVisible(false)}
        width={1200}
        footer={[
          <Button key="close" onClick={() => setDetailModalVisible(false)}>
            关闭
          </Button>
        ]}
        style={{ top: 20 }}
      >
        <Row gutter={24}>
          {/* 左侧：PDF预览 */}
          {pdfUrl && (
            <Col xs={24} lg={12}>
              <div style={{ 
                height: '75vh', 
                border: '1px solid #d9d9d9', 
                borderRadius: '8px',
                overflow: 'hidden',
                background: '#f5f5f5'
              }}>
                <iframe
                  src={pdfUrl}
                  style={{
                    width: '100%',
                    height: '100%',
                    border: 'none'
                  }}
                  title="PDF预览"
                />
              </div>
            </Col>
          )}

          {/* 右侧：详细信息 */}
          <Col xs={24} lg={pdfUrl ? 12 : 24}>
            <div style={{ maxHeight: '75vh', overflowY: 'auto', paddingRight: '8px' }}>
          {/* 综合评分 */}
          <div style={{
            background: 'linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%)',
            padding: '24px',
            borderRadius: '12px',
            marginBottom: '24px',
            textAlign: 'center'
          }}>
            <div style={{
              fontSize: '56px',
              fontWeight: 'bold',
              color: getScoreColor(total_score),
              marginBottom: '8px'
            }}>
              {total_score}分
            </div>
            <Text type="secondary" style={{ fontSize: '16px' }}>综合匹配度评分</Text>
          </div>

          {/* 基本信息 */}
          <Collapse defaultActiveKey={['1', '2', '3', '4']} ghost>
            <Panel header={<Text strong><UserOutlined /> 基本信息</Text>} key="1">
              <Row gutter={[16, 16]}>
                <Col span={12}>
                  <Text type="secondary">姓名：</Text>
                  <Text strong>{basic_info.name || '未识别'}</Text>
                </Col>
                <Col span={12}>
                  <Text type="secondary">电话：</Text>
                  <Text copyable>{basic_info.phone || '未提供'}</Text>
                </Col>
                <Col span={12}>
                  <Text type="secondary">邮箱：</Text>
                  <Text copyable>{basic_info.email || '未提供'}</Text>
                </Col>
                <Col span={12}>
                  <Text type="secondary">地址：</Text>
                  <Text>{basic_info.address || '未提供'}</Text>
                </Col>
                <Col span={12}>
                  <Text type="secondary">学历：</Text>
                  <Tag color="purple">{background.education || '未明确'}</Tag>
                </Col>
                <Col span={12}>
                  <Text type="secondary">工作年限：</Text>
                  <Tag color="orange">{background.work_years || '未明确'}</Tag>
                </Col>
              </Row>
            </Panel>

            <Panel header={<Text strong><FileTextOutlined /> 求职意向</Text>} key="2">
              <Row gutter={[16, 16]}>
                <Col span={12}>
                  <Text type="secondary">目标职位：</Text>
                  <Tag color="blue">{job_info.position || '未明确'}</Tag>
                </Col>
                <Col span={12}>
                  <Text type="secondary">期望薪资：</Text>
                  <Tag color="green">{job_info.salary || '面议'}</Tag>
                </Col>
              </Row>
            </Panel>

            <Panel header={<Text strong><StarOutlined /> 专业技能 ({background.skills?.length || 0}项)</Text>} key="3">
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                {background.skills && background.skills.length > 0 ? (
                  background.skills.map((skill, idx) => (
                    <Tag key={idx} color="blue">{skill}</Tag>
                  ))
                ) : (
                  <Text type="secondary">未提取到技能信息</Text>
                )}
              </div>
            </Panel>

            <Panel header={<Text strong><BulbOutlined /> 项目经验 ({background.projects?.length || 0}个)</Text>} key="4">
              {background.projects && background.projects.length > 0 ? (
                <Space direction="vertical" style={{ width: '100%' }}>
                  {background.projects.map((project, idx) => (
                    <div key={idx} style={{
                      padding: '12px',
                      background: '#f5f5f5',
                      borderRadius: '8px',
                      borderLeft: '3px solid #1890ff'
                    }}>
                      <Text strong>{idx + 1}. {project}</Text>
                    </div>
                  ))}
                </Space>
              ) : (
                <Text type="secondary">未提取到项目信息</Text>
              )}
            </Panel>
          </Collapse>

          <Divider />

          {/* 匹配度详情 */}
          <div style={{ marginTop: '24px' }}>
            <Title level={5}>
              <TrophyOutlined /> 匹配度详细分析
            </Title>
            
            <Space direction="vertical" size="middle" style={{ width: '100%', marginTop: '16px' }}>
              {/* 技能匹配 */}
              <div>
                <div style={{ marginBottom: '8px' }}>
                  <Text strong>技能匹配度：</Text>
                  <Text style={{ color: getScoreColor(skill_match.score), marginLeft: '8px', fontSize: '18px', fontWeight: 'bold' }}>
                    {skill_match.score}分
                  </Text>
                </div>
                <Progress 
                  percent={skill_match.score} 
                  strokeColor={getScoreColor(skill_match.score)}
                  strokeWidth={12}
                />
                <div style={{ marginTop: '8px' }}>
                  <Text type="secondary">{skill_match.details}</Text>
                </div>
                {skill_match.matched_skills && skill_match.matched_skills.length > 0 && (
                  <div style={{ marginTop: '8px' }}>
                    <Text type="secondary">匹配技能：</Text>
                    {skill_match.matched_skills.map((skill, idx) => (
                      <Tag key={idx} color="success" style={{ marginTop: 4 }}>{skill}</Tag>
                    ))}
                  </div>
                )}
                {skill_match.missing_skills && skill_match.missing_skills.length > 0 && (
                  <div style={{ marginTop: '8px' }}>
                    <Text type="secondary">待提升技能：</Text>
                    {skill_match.missing_skills.map((skill, idx) => (
                      <Tag key={idx} color="error" style={{ marginTop: 4 }}>{skill}</Tag>
                    ))}
                  </div>
                )}
              </div>

              {/* 经验匹配 */}
              <div>
                <div style={{ marginBottom: '8px' }}>
                  <Text strong>经验匹配度：</Text>
                  <Text style={{ color: getScoreColor(experience_match.score), marginLeft: '8px', fontSize: '18px', fontWeight: 'bold' }}>
                    {experience_match.score}分
                  </Text>
                </div>
                <Progress 
                  percent={experience_match.score} 
                  strokeColor={getScoreColor(experience_match.score)}
                  strokeWidth={12}
                />
                <div style={{ marginTop: '8px' }}>
                  <Text type="secondary">{experience_match.details}</Text>
                </div>
              </div>

              {/* 职位匹配 */}
              <div>
                <div style={{ marginBottom: '8px' }}>
                  <Text strong>职位匹配度：</Text>
                  <Text style={{ color: getScoreColor(position_match.score), marginLeft: '8px', fontSize: '18px', fontWeight: 'bold' }}>
                    {position_match.score}分
                  </Text>
                </div>
                <Progress 
                  percent={position_match.score} 
                  strokeColor={getScoreColor(position_match.score)}
                  strokeWidth={12}
                />
                <div style={{ marginTop: '8px' }}>
                  <Text type="secondary">{position_match.details}</Text>
                </div>
              </div>
            </Space>
          </div>

          {/* 改进建议 */}
          {recommendations && recommendations.length > 0 && (
            <div style={{ marginTop: '24px' }}>
              <Title level={5}>
                <BulbOutlined /> AI改进建议
              </Title>
              <ul style={{ marginTop: '12px', paddingLeft: '20px' }}>
                {recommendations.map((rec, idx) => (
                  <li key={idx} style={{ marginBottom: '8px' }}>
                    <Text>{rec}</Text>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* 面试建议 */}
          <div style={{ marginTop: '24px' }}>
            <Title level={5}>
              <CheckCircleOutlined /> 面试建议
            </Title>
            {total_score >= 80 ? (
              <Alert
                message="强烈推荐进入下一轮面试"
                description="候选人综合素质优秀，技能和经验与岗位高度匹配，建议优先安排面试。"
                type="success"
                showIcon
                style={{ marginTop: '12px' }}
              />
            ) : total_score >= 60 ? (
              <Alert
                message="建议进入下一轮面试"
                description="候选人基本符合岗位要求，建议安排面试进一步评估。"
                type="warning"
                showIcon
                style={{ marginTop: '12px' }}
              />
            ) : (
              <Alert
                message="暂不推荐进入面试"
                description="候选人与岗位匹配度较低，建议继续筛选其他候选人。"
                type="error"
                showIcon
                style={{ marginTop: '12px' }}
              />
            )}
          </div>
            </div>
          </Col>
        </Row>
      </Modal>
    );
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header className="app-header">
        <div className="header-content">
          <div className="logo-section">
            <div className="logo-icon">
              <RobotOutlined />
            </div>
            <Title level={3} className="app-title">
              AI智能简历分析系统
            </Title>
          </div>
          <div className="header-stats">
            <div className="stat-item">
              <CheckCircleOutlined />
              <span>智能解析</span>
            </div>
            <div className="stat-item">
              <BarChartOutlined />
              <span>精准匹配</span>
            </div>
            <div className="stat-item">
              <BulbOutlined />
              <span>智能排序</span>
            </div>
          </div>
        </div>
      </Header>
      
      <Content className="app-container">
        <Spin spinning={loading} tip={loading ? "AI正在分析简历，请稍候..." : ""} className="loading-overlay">
          {/* 欢迎区域 */}
          {!jobRequirement && renderWelcomeSection()}

          {/* 步骤1: 岗位需求配置 */}
          {!jobRequirement && (
            <div className="modern-card fade-in-up">
              <div className="card-header">
                <div className="card-title">
                  <FileTextOutlined />
                  步骤1：配置岗位需求
                </div>
                <div className="card-subtitle">先设置招聘岗位信息，系统将根据此标准筛选候选人</div>
              </div>
              <div className="form-section">
                <Form onFinish={handleSaveJobRequirement} layout="vertical">
                  <Row gutter={16}>
                    <Col xs={24} md={12}>
                      <Form.Item
                        name="job_title"
                        label="职位名称"
                        rules={[{ required: true, message: '请输入职位名称' }]}
                      >
                        <Input 
                          placeholder="例：Python后端工程师" 
                          className="form-input"
                          size="large"
                        />
                      </Form.Item>
                    </Col>
                    <Col xs={24} md={12}>
                      <Form.Item
                        name="experience_level"
                        label="经验要求"
                        rules={[{ required: true, message: '请输入经验要求' }]}
                      >
                        <Input 
                          placeholder="例：3-5年工作经验" 
                          className="form-input"
                          size="large"
                        />
                      </Form.Item>
                    </Col>
                  </Row>
                  
                  <Form.Item
                    name="required_skills"
                    label="技能要求"
                    rules={[{ required: true, message: '请输入技能要求' }]}
                  >
                    <Input 
                      placeholder="例：Python, FastAPI, MySQL, Redis, Docker" 
                      className="form-input"
                      size="large"
                    />
                  </Form.Item>
                  
                  <Form.Item
                    name="job_description"
                    label="职位描述"
                    rules={[{ required: true, message: '请输入职位描述' }]}
                  >
                    <TextArea 
                      rows={4} 
                      placeholder="请详细描述岗位职责、任职要求、工作内容等信息..."
                      className="form-input"
                    />
                  </Form.Item>
                  
                  <Form.Item>
                    <Button 
                      type="primary" 
                      htmlType="submit" 
                      size="large"
                      className="submit-button"
                      icon={<CheckCircleOutlined />}
                    >
                      保存岗位需求，进入下一步
                    </Button>
                  </Form.Item>
                </Form>
              </div>
            </div>
          )}

          {/* 步骤2: 批量上传简历 */}
          {jobRequirement && (
            <>
              {/* 显示已保存的岗位需求 */}
              <div className="modern-card fade-in-up">
                <div className="card-header">
                  <div className="card-title">
                    <CheckCircleOutlined style={{ color: '#52c41a' }} />
                    当前岗位需求
                  </div>
                  <Button 
                    type="link" 
                    onClick={() => {
                      setJobRequirement(null);
                      setCandidates([]);
                    }}
                  >
                    重新配置
                  </Button>
                </div>
                <div style={{ padding: '0 24px 24px' }}>
                  <Row gutter={[16, 16]}>
                    <Col xs={24} md={12}>
                      <Text strong>职位名称：</Text>
                      <Tag color="blue" style={{ marginLeft: 8 }}>{jobRequirement.job_title}</Tag>
                    </Col>
                    <Col xs={24} md={12}>
                      <Text strong>经验要求：</Text>
                      <Tag color="orange" style={{ marginLeft: 8 }}>{jobRequirement.experience_level}</Tag>
                    </Col>
                    <Col xs={24}>
                      <Text strong>技能要求：</Text>
                      <div style={{ marginTop: 8 }}>
                        {jobRequirement.required_skills.split(',').map((skill, idx) => (
                          <Tag key={idx} color="purple" style={{ marginBottom: 4 }}>
                            {skill.trim()}
                          </Tag>
                        ))}
                      </div>
                    </Col>
                  </Row>
                </div>
              </div>

              {/* 批量上传区域 */}
              <div className="modern-card fade-in-up">
                <div className="card-header">
                  <div className="card-title">
                    <InboxOutlined />
                    步骤2：批量上传候选人简历
                  </div>
                  <div className="card-subtitle">
                    支持同时上传多份PDF简历，AI将自动分析并按匹配度排序
                    {candidates.length > 0 && (
                      <Tag color="green" style={{ marginLeft: 12 }}>
                        已分析 {candidates.length} 位候选人
                      </Tag>
                    )}
                  </div>
                </div>
                <div style={{ padding: '0 24px 24px' }}>
                  <Dragger
                    name="file"
                    accept=".pdf"
                    multiple
                    beforeUpload={(file, fileList) => {
                      handleBatchUpload(fileList);
                      return false;
                    }}
                    showUploadList={false}
                    style={{
                      border: '2px dashed #e1e8ed',
                      borderRadius: '12px',
                      background: 'linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)',
                    }}
                  >
                    <div style={{ padding: '60px 40px' }}>
                      <div style={{ fontSize: '64px', color: '#667eea', marginBottom: '16px' }}>
                        <InboxOutlined />
                      </div>
                      <div style={{ fontSize: '18px', fontWeight: 600, color: '#2c3e50', marginBottom: '8px' }}>
                        点击选择或拖拽多份PDF简历文件
                      </div>
                      <div style={{ color: '#7f8c8d', fontSize: '14px' }}>
                        支持批量上传，AI将自动分析并按匹配度排序
                      </div>
                    </div>
                  </Dragger>
                </div>
              </div>
            </>
          )}

          {/* 步骤3: 显示候选人列表（按评分排序） */}
          {candidates.length > 0 && renderCandidatesList()}
        </Spin>

        {/* 候选人详情弹窗 */}
        {renderDetailModal()}
      </Content>
    </Layout>
  );
}

export default App;
