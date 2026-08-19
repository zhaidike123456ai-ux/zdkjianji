import {createContext, useContext} from "react";

export type KnowledgeCardTheme = {
  ink: string;
  blue: string;
  paleBlue: string;
  danger: string;
  lightTop: string;
  lightBottom: string;
  darkAccent: string;
  captionAccent: string;
};

export const defaultKnowledgeCardTheme: KnowledgeCardTheme = {
  ink: "#101828",
  blue: "#2488E8",
  paleBlue: "#EAF5FF",
  danger: "#F14B53",
  lightTop: "#F7FBFF",
  lightBottom: "#EAF6FF",
  darkAccent: "#48F27A",
  captionAccent: "#F9E547",
};

const ThemeContext = createContext(defaultKnowledgeCardTheme);

export const KnowledgeCardThemeProvider: React.FC<{
  theme?: KnowledgeCardTheme;
  children: React.ReactNode;
}> = ({theme = defaultKnowledgeCardTheme, children}) => (
  <ThemeContext.Provider value={theme}>{children}</ThemeContext.Provider>
);

export const useKnowledgeCardTheme = () => useContext(ThemeContext);

