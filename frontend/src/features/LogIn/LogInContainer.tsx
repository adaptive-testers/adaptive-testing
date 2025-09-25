import { MdOutlineMailOutline } from "react-icons/md";
import { TbLockPassword } from "react-icons/tb";
import { IoEyeOffOutline, IoEyeOutline } from "react-icons/io5";

import { useState } from "react";

import google from "./icons/google.svg";
import microsoft from "./icons/microsoft.svg";

export default function LogInContainer() {
  const [showPassword, setShowPassword] = useState(false);
  const handlePasswordToggle = () => setShowPassword((prev) => !prev);

  const [keepSignedIn, setKeepSignedIn] = useState(false);
  const toggleCheckbox = () => setKeepSignedIn((prev) => !prev);

  return (
    <div className="Log-In w-[1280px] h-[832px] bg-[#000000]">
      <div className="Sign-Up-Box relative flex justify-center items-center p-[40px] gap-[10px] w-[482px] h-[631px] left-[50%] top-[50%] -translate-x-[50%] -translate-y-[50%] border border-[#282828] rounded-[15px]">
        <div className="Frame-25 absolute flex flex-col items-start gap-[40px] w-[402px] h-[551px]">
          <div className="Frame-19 flex flex-col items-center gap-[40px] w-[402px] h-[335px]">
            <h1 className="Log-In w-[120px] h-[31px] flex items-center justify-center font-geist font-medium text-[32px] leading-[42px] flex items-center text-center tracking-[0.5px] text-[#ffffff]">
              Log In
            </h1>
            <div className="Frame-18 flex flex-col items-start gap-[32px] w-[402px] h-[264px]">
              <div className="Frame-17 flex flex-col items-start gap-[24px] w-[402px] h-[192px]">
                <form className="Frame-13 flex flex-col items-start gap-[8px] w-[402px] h-[64px]">
                  <label
                    htmlFor="email-input"
                    className="Email w-[38px] h-[16px] font-geist font-normal text-[14px] leading-[16px] flex items-center tracking-[0.5px] text-[#8E8E8E]"
                  >
                    Email
                  </label>
                  <div className="Frame-10 flex flex-row items-center gap-[12px] w-[402px] h-[40px] px-[14px] py-[11px] bg-[#0A0A0A] border border-[#282828] shadow-[0_4px_4px_#00000040] rounded-[8px] focus-within:border-[rgba(174,58,58,0.4)]">
                    <input
                      id="email-input"
                      type="email"
                      className="peer bg-transparent flex-1 text-white text-[14px] outline-none focus:border-[rgba(174,58,58,0.4)] focus:outline-none"
                      placeholder="Enter your email"
                    />
                    <MdOutlineMailOutline className="order-first scale-170 w-[10px] h-[12px] mx-auto text-[#8e8e8e] peer-focus:text-white text-sm pointer-events-none" />
                  </div>
                </form>
                <form className="Frame-14 flex flex-col items-start gap-[8px] w-[402px] h-[64px]">
                  <label
                    htmlFor="password-input"
                    className="Password w-[67px] h-[16px] font-geist font-normal text-[14px] leading-[16px] flex items-center tracking-[0.5px] text-[#8E8E8E]"
                  >
                    Password
                  </label>
                  <div className="Frame-10 flex flex-row items-center gap-[12px] w-[402px] h-[40px] px-[14px] py-[11px] bg-[#0A0A0A] border border-[#282828] shadow-[0_4px_4px_#00000040] rounded-[8px] focus-within:border-[rgba(174,58,58,0.4)]">
                    <input
                      id="password-input"
                      type={showPassword ? "text" : "password"}
                      className="peer bg-transparent flex-1 text-white text-[14px] outline-none focus:border-[rgba(174,58,58,0.4)] focus:outline-none"
                      placeholder="Enter your password"
                    />
                    <TbLockPassword className="flex order-first justify-center scale-170 w-[11px] h-[12px] gap-[10px] mx-auto text-[#8e8e8e] peer-focus:text-white text-sm pointer-events-none" />
                    <button
                      type="button"
                      aria-label={
                        showPassword ? "Hide password" : "Show password"
                      }
                      onClick={handlePasswordToggle}
                      className="w-[16px] h-[13px] mx-auto scale-125 text-[#8e8e8e] text-sm cursor-pointer hover:text-white transition-colors duration-300 bg-transparent border-none p-0 focus:outline-none focus-visible:ring-2 focus-visible:ring-[#ae3a3a] rounded"
                    >
                      {showPassword ? <IoEyeOutline /> : <IoEyeOffOutline />}
                    </button>
                  </div>
                </form>
                <div className="Frame-39 flex items-center gap-[8px] w-[140px] h-[16px] text-[#8E8E8E] transition duration-500 ease-in-out hover:scale-102 hover:text-white">
                  <button
                    type="button"
                    onClick={toggleCheckbox}
                    className={`flex items-center gap-[10px] w-[14px] h-[14px] p-[3px] rounded-[4px] border border-[#282828] ${
                      keepSignedIn ? "bg-[#EF6262]" : "bg-[#0A0A0A]"
                    }`}
                  ></button>
                  <p
                    onClick={toggleCheckbox}
                    className="Forgot-pass w-[120px] h-[16px] font-geist font-normal text-[12px] leading-[16px] flex items-center tracking-[0.5px]"
                  >
                    Keep me signed in
                  </p>
                </div>
              </div>
              <button className="Frame-8 flex justify-center items-center gap-[10px] w-[402px] h-[40px] bg-[#EF6262] rounded-[8px] hover:scale-102 duration-500">
                <p className="Sign-in w-[48px] h-[16px] font-geist font-normal text-[14px] leading-[16px] flex items-center tracking-[0.5px] text-[#ffffff]">
                  Sign In
                </p>
              </button>
            </div>
          </div>
          <div className="Frame-26 flex justify-center items-center gap-[10px] w-[402px] h-[16px]">
            <div className="Rectangle-2 w-[182px] h-[1px] bg-[#232323] flex-grow"></div>
            <p className="OR w-[18px] h-[16px] font-geist font-semibold text-[12px] leading-[16px] flex items-center text-center tracking-[0.5px] text-[#8E8E8E]">
              OR
            </p>
            <div className="Rectangle-1 w-[182px] h-[1px] bg-[#232323] flex-grow"></div>
          </div>
          <div className="Frame-24 flex flex-col items-center gap-[40px] w-[402px] h-[120px]">
            <div className="Frame-27 flex justify-between items-center gap-[24px] w-[402px] h-[40px]">
              <button className="Frame-20 flex justify-center items-center gap-[10px] w-[192px] h-[40px] px-[14px] mx-auto border border-[#242424] rounded-[8px] hover:border-white hover:scale-102 duration-500">
                <img
                  className="flex items-center gap-[12px] w-[16px] h-[16px]"
                  src={google}
                ></img>
              </button>
              <button className="Frame-24 flex justify-center items-center gap-[10px] w-[192px] h-[40px] px-[14px] mx-auto border border-[#242424] rounded-[8px] hover:border-white hover:scale-102 duration-50">
                <img
                  className="flex items-center gap-[12px] w-[16px] h-[16px]"
                  src={microsoft}
                ></img>
              </button>
            </div>
          </div>
          <div className="Frame-7 flex flex-col justify-center items-center gap-[21px] w-[402px] h-[40px]">
            <p className="font-geist font-normal text-[14px] leading-[16px] flex items-center tracking-[0.5px]">
              <span className="text-[#EF6262] underline">Can't log in?</span>
              <span className="mx-1 text-[#ededed]">•</span>
              <span className="text-[#EF6262] underline">
                Create an account
              </span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
