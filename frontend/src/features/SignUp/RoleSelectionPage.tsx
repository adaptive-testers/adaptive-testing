import { useState } from 'react'
import { FaChalkboardTeacher } from 'react-icons/fa'
import { TbSchool } from 'react-icons/tb'

export default function RoleSelectionPage() {
    const [selectedRole, setSelectedRole] = useState<'student' | 'instructor' | null>(null)

    const handleRoleSelect = (role: 'student' | 'instructor') => {
        setSelectedRole(role)
    }

    const handleContinue = () => {
        if (selectedRole) {
            console.log('Selected role:', selectedRole)
            // TODO: Navigate to next step or handle role selection
        }
    }

    return (
        <div className="bg-[#0A0A0A] w-[600px] h-[400px] border-[2px] border-[#282828] rounded-[15px] flex flex-col items-center justify-center p-6">
                {/* Title */}
                <h1 className="text-white geist-font text-[28px] font-[480] mb-6 text-center">
                    Select Your Role
                </h1>

                {/* Role Options */}
                <div className="flex gap-6 mb-4 w-full max-w-lg">
                    {/* Student Option */}
                    <div 
                        className={`flex-1 bg-[#0A0A0A] border-[2px] border-[#282828] rounded-lg p-10 cursor-pointer transition-all duration-350 hover:border-[rgba(174,58,58,0.4)] group ${
                            selectedRole === 'student' ? 'border-[rgba(174,58,58,0.4)] ' : ''
                        }`}
                        onClick={() => handleRoleSelect('student')}
                    >
                        <div className="flex flex-col items-center">
                            <TbSchool className={`text-6xl mb-4 transition-colors duration-200 ${
                                selectedRole === 'student' ? 'text-[#EF6262]' : 'text-[#8E8E8E] group-hover:text-[#EF6262]'
                            }`} />
                            <span className={`geist-font text-xl font-[450] transition-colors duration-200 ${
                                selectedRole === 'student' ? 'text-white' : 'text-[#8E8E8E] group-hover:text-white'
                            }`}>Student</span>
                        </div>
                    </div>

                    {/* Instructor Option */}
                    <div 
                        className={`flex-1 bg-[#0A0A0A] border-[2px] border-[#282828] rounded-lg p-10 cursor-pointer transition-all duration-350 hover:border-[rgba(174,58,58,0.4)] group ${
                            selectedRole === 'instructor' ? 'border-[rgba(174,58,58,0.4)]' : ''
                        }`}
                        onClick={() => handleRoleSelect('instructor')}
                    >
                        <div className="flex flex-col items-center">
                            <FaChalkboardTeacher className={`text-6xl mb-4 transition-colors duration-200 ${
                                selectedRole === 'instructor' ? 'text-[#EF6262]' : 'text-[#8E8E8E] group-hover:text-[#EF6262]'
                            }`} />
                            <span className={`geist-font text-xl font-[450] transition-colors duration-200 ${
                                selectedRole === 'instructor' ? 'text-white' : 'text-[#8E8E8E] group-hover:text-white'
                            }`}>Instructor</span>
                        </div>
                    </div>
                </div>

                {/* Continue Button */}
                <div className="relative">
                    <button 
                        onClick={handleContinue}
                        disabled={!selectedRole}
                        className={`text-white w-[105px] h-[35px] rounded-[6px] tracking-wider geist-font font-[250] text-[13px] mt-4 cursor-pointer transition-all duration-200 origin-center will-change-transform hover:bg-[#C04A4A] hover:shadow-[0_2px_12px_0_rgba(192,74,74,0.25)] ${
                            !selectedRole ? 'bg-[#EF6262] cursor-not-allowed' : 'bg-[#EF6262]'
                        }`}
                    >
                        Continue
                    </button>
                </div>
        </div>
    )
}